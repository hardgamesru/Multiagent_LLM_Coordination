from __future__ import annotations

from sandbox_runner import run_code_in_sandbox
from tasks import Task, get_tasks


NAIVE_SOLUTIONS = {
    "parse_csv_line": '''def parse_csv_line(line: str) -> list[str]:
    return line.split(",")
''',
    "top_k_frequent": '''def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    counts = {}
    for word in words:
        word = word.lower()
        counts[word] = counts.get(word, 0) + 1
    return [word for word, _count in sorted(counts.items(), key=lambda item: -item[1])[:k]]
''',
    "detect_cycle": '''def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    visiting = set()
    visited = set()
    def visit(node):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dep in dependencies[node]:
            if visit(dep):
                return True
        visiting.remove(node)
        visited.add(node)
        return False
    return any(visit(node) for node in dependencies)
''',
    "normalize_email": '''def normalize_email(email: str) -> str:
    email = email.strip()
    local, domain = email.split("@", 1)
    if not local or not domain or "." not in domain:
        raise ValueError("invalid email")
    return local + "@" + domain.lower()
''',
    "merge_intervals": '''def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    for start, end in intervals:
        if start > end:
            raise ValueError("invalid interval")
    intervals = sorted(intervals)
    result = []
    for start, end in intervals:
        if not result or start >= result[-1][1]:
            result.append((start, end))
        else:
            result[-1] = (result[-1][0], max(result[-1][1], end))
    return result
''',
}


def main() -> None:
    tasks_by_name: dict[str, Task] = {task.name: task for task in get_tasks()}
    failed_to_reject = []

    for task_name, code in NAIVE_SOLUTIONS.items():
        task = tasks_by_name[task_name]
        result = run_code_in_sandbox(code, task.hidden_tests)
        if result.success:
            failed_to_reject.append(task_name)
            print(f"FAIL: hidden tests accepted naive solution for {task_name}")
        else:
            print(f"OK: hidden tests rejected naive solution for {task_name}")

    if failed_to_reject:
        joined = ", ".join(failed_to_reject)
        raise SystemExit(f"Quality check failed for: {joined}")

    print("All selected naive solutions were rejected by hidden tests.")


if __name__ == "__main__":
    main()
