from __future__ import annotations

import os
import re
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    model_name: str

    def __init__(self) -> None:
        self.last_input_tokens = 0
        self.last_output_tokens = 0
        self.last_total_tokens = 0
        self.cumulative_input_tokens = 0
        self.cumulative_output_tokens = 0
        self.cumulative_total_tokens = 0

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError

    def get_usage_totals(self) -> tuple[int, int, int]:
        return (
            self.cumulative_input_tokens,
            self.cumulative_output_tokens,
            self.cumulative_total_tokens,
        )

    def get_usage_delta(self, start: tuple[int, int, int]) -> tuple[int, int, int]:
        current = self.get_usage_totals()
        return tuple(current[index] - start[index] for index in range(3))

    def _record_usage(self, input_tokens: int = 0, output_tokens: int = 0, total_tokens: int = 0) -> None:
        if total_tokens == 0 and (input_tokens or output_tokens):
            total_tokens = input_tokens + output_tokens
        self.last_input_tokens = input_tokens
        self.last_output_tokens = output_tokens
        self.last_total_tokens = total_tokens
        self.cumulative_input_tokens += input_tokens
        self.cumulative_output_tokens += output_tokens
        self.cumulative_total_tokens += total_tokens


class GigaChatClient(BaseLLMClient):
    def __init__(
        self,
        auth_key: str,
        model: str,
        verify_ssl: bool = False,
        timeout: int = 60,
    ) -> None:
        super().__init__()
        self.auth_key = auth_key
        self.model_name = model
        self.verify_ssl = verify_ssl
        self.timeout = timeout

    @classmethod
    def from_env(cls, model: str | None = None) -> "GigaChatClient | None":
        auth_key = os.getenv("GIGACHAT_AUTH_KEY")
        if not auth_key:
            return None

        selected_model = model or os.getenv("GIGACHAT_MODEL", "GigaChat-2")
        verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL", "false").lower() in {"1", "true", "yes"}
        timeout = int(os.getenv("GIGACHAT_TIMEOUT", "60"))
        return cls(
            auth_key=auth_key,
            model=selected_model,
            verify_ssl=verify_ssl,
            timeout=timeout,
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        self._record_usage(0, 0, 0)
        try:
            from gigachat import GigaChat
            from gigachat.models import Chat, Messages, MessagesRole
        except ImportError as exc:
            raise RuntimeError("The gigachat package is not installed.") from exc

        chat = Chat(
            model=self.model_name,
            messages=[
                Messages(role=MessagesRole.SYSTEM, content=system_prompt),
                Messages(role=MessagesRole.USER, content=user_prompt),
            ],
        )
        try:
            with GigaChat(
                credentials=self.auth_key,
                verify_ssl_certs=self.verify_ssl,
                timeout=self.timeout,
            ) as giga:
                response = giga.chat(chat)
        except Exception as exc:
            safe_error = self._sanitize_error(exc)
            raise RuntimeError(
                f"GigaChat request failed for model {self.model_name}: {safe_error}"
            ) from exc

        usage = getattr(response, "usage", None)
        input_tokens = self._get_usage_value(usage, "prompt_tokens", "input_tokens")
        output_tokens = self._get_usage_value(usage, "completion_tokens", "output_tokens")
        total_tokens = self._get_usage_value(usage, "total_tokens")
        self._record_usage(input_tokens, output_tokens, total_tokens)
        return response.choices[0].message.content

    @staticmethod
    def _get_usage_value(usage: object, *names: str) -> int:
        if usage is None:
            return 0
        for name in names:
            value = getattr(usage, name, None)
            if value is not None:
                return int(value)
        if isinstance(usage, dict):
            for name in names:
                value = usage.get(name)
                if value is not None:
                    return int(value)
        return 0

    def get_available_models(self) -> list[str]:
        try:
            from gigachat import GigaChat
        except ImportError as exc:
            raise RuntimeError("The gigachat package is not installed.") from exc

        try:
            with GigaChat(
                credentials=self.auth_key,
                verify_ssl_certs=self.verify_ssl,
                timeout=self.timeout,
            ) as giga:
                response = giga.get_models()
        except Exception as exc:
            safe_error = self._sanitize_error(exc)
            raise RuntimeError(f"GigaChat model list request failed: {safe_error}") from exc

        result = []
        for model in getattr(response, "data", []):
            model_id = getattr(model, "id_", None) or getattr(model, "id", None)
            if model_id:
                result.append(str(model_id))
        return result

    def _sanitize_error(self, exc: Exception) -> str:
        text = str(exc)
        if self.auth_key:
            text = text.replace(self.auth_key, "[hidden]")
        text = re.sub(r"(?i)(authorization[\"':= ]+)([^,\\s}]+)", r"\1[hidden]", text)
        text = re.sub(r"(?i)(credentials[\"':= ]+)([^,\\s}]+)", r"\1[hidden]", text)
        return f"{type(exc).__name__}: {text[:500]}"


class MockLLMClient(BaseLLMClient):
    def __init__(self) -> None:
        super().__init__()
        self.model_name = "mock"

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        self._record_usage(0, 0, 0)
        lowered_system = system_prompt.lower()
        solution = self._solution_for_prompt(user_prompt)
        is_tester = "errors" in lowered_system and "ok" in lowered_system
        is_developer = "python" in lowered_system and "markdown" in lowered_system
        wants_final_code = any(
            marker in user_prompt
            for marker in ("Code:", "Initial code:", "Selected shortest", "Return the final")
        )

        if is_tester:
            return "OK"
        if solution and (is_developer or wants_final_code):
            return solution
        if solution and "Candidate test results" in user_prompt:
            return solution
        return "Requirements, edge cases, and expected behavior are defined by the task statement."

    def _solution_for_prompt(self, prompt: str) -> str:
        function_name = self._detect_function_name(prompt)
        solutions = {
            "normalize_email": '''def normalize_email(email: str) -> str:
    email = email.strip()
    if email.count("@") != 1:
        raise ValueError("email must contain exactly one @")
    local, domain = email.split("@")
    if not local or not domain or "." not in domain:
        raise ValueError("invalid email")
    return local + "@" + domain.lower()
''',
            "parse_csv_line": '''def parse_csv_line(line: str) -> list[str]:
    result = []
    field = []
    in_quotes = False
    index = 0
    while index < len(line):
        char = line[index]
        if char == '"':
            if in_quotes and index + 1 < len(line) and line[index + 1] == '"':
                field.append('"')
                index += 1
            else:
                in_quotes = not in_quotes
        elif char == "," and not in_quotes:
            result.append("".join(field))
            field = []
        else:
            field.append(char)
        index += 1
    result.append("".join(field))
    return result
''',
            "merge_intervals": '''def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    for start, end in intervals:
        if start > end:
            raise ValueError("interval start cannot exceed end")
    sorted_intervals = sorted(intervals, key=lambda item: item[0])
    merged = []
    for start, end in sorted_intervals:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    return merged
''',
            "calculate_cart_total": '''def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    total = 0.0
    food_total = 0.0
    for item in items:
        if "price" not in item or "quantity" not in item or "category" not in item:
            raise ValueError("item must contain price, quantity, and category")
        price = item["price"]
        quantity = item["quantity"]
        category = item["category"]
        if price < 0 or quantity <= 0:
            raise ValueError("invalid price or quantity")
        line_total = price * quantity
        total += line_total
        if category == "food":
            food_total += line_total
    if promo_code == "SALE10":
        total *= 0.9
    elif promo_code == "FOOD5":
        total -= food_total * 0.05
    return round(total, 2)
''',
            "top_k_frequent": '''def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    counts = {}
    for word in words:
        normalized = word.lower()
        counts[normalized] = counts.get(normalized, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in ordered[:k]]
''',
            "detect_cycle": '''def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    nodes = set(dependencies)
    for deps in dependencies.values():
        nodes.update(deps)
    visiting = set()
    visited = set()

    def visit(node):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dep in dependencies.get(node, []):
            if visit(dep):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in nodes)
''',
            "analyze_logs": '''def analyze_logs(lines: list[str]) -> dict:
    import re
    pattern = re.compile(r"^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2} (INFO|WARNING|ERROR) (\\S+) (\\d{3})$")
    by_level = {}
    by_endpoint = {}
    total = 0
    errors = 0
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        level, endpoint, _status = match.groups()
        total += 1
        by_level[level] = by_level.get(level, 0) + 1
        by_endpoint[endpoint] = by_endpoint.get(endpoint, 0) + 1
        if level == "ERROR":
            errors += 1
    most_common_endpoint = None
    if by_endpoint:
        most_common_endpoint = sorted(by_endpoint.items(), key=lambda item: (-item[1], item[0]))[0][0]
    return {
        "total": total,
        "by_level": by_level,
        "errors": errors,
        "most_common_endpoint": most_common_endpoint,
    }
''',
            "group_by_category": '''def group_by_category(items: list[dict]) -> dict[str, list[dict]]:
    grouped = {}
    for item in items:
        category = item.get("category", "unknown")
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(item)
    return grouped
''',
            "resolve_build_order": '''def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    nodes = set(dependencies)
    for deps in dependencies.values():
        nodes.update(deps)
    outgoing = {node: set() for node in nodes}
    indegree = {node: 0 for node in nodes}
    for task, deps in dependencies.items():
        for dep in deps:
            outgoing.setdefault(dep, set()).add(task)
            indegree[task] = indegree.get(task, 0) + 1
            indegree.setdefault(dep, 0)
    available = sorted(node for node, degree in indegree.items() if degree == 0)
    result = []
    while available:
        node = available.pop(0)
        result.append(node)
        for dependent in sorted(outgoing.get(node, set())):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                available.append(dependent)
        available.sort()
    if len(result) != len(nodes):
        raise ValueError("dependency cycle detected")
    return result
''',
        }
        return solutions.get(function_name, "")

    @staticmethod
    def _detect_function_name(prompt: str) -> str:
        for name in (
            "normalize_email",
            "parse_csv_line",
            "merge_intervals",
            "calculate_cart_total",
            "top_k_frequent",
            "detect_cycle",
            "analyze_logs",
            "group_by_category",
            "resolve_build_order",
        ):
            if name in prompt:
                return name
        return ""
