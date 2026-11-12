from __future__ import annotations

import ast
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path


def ensure_directories(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_run_id() -> str:
    return uuid.uuid4().hex[:12]


def safe_filename_part(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9_\-]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_")


def extract_python_code(text: str) -> str:
    """Extract a Python function from a raw LLM response."""
    if not text:
        return ""

    blocks = re.findall(r"```(?:python|py)?[ \t]*\r?\n(.*?)```", text, re.IGNORECASE | re.DOTALL)
    for candidate in blocks + [text]:
        try:
            ast.parse(candidate.strip())
            return candidate.strip()
        except SyntaxError:
            pass

    fenced_blocks = re.findall(r"```(?:python|py)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    candidate = fenced_blocks[0] if fenced_blocks else text
    candidate = candidate.strip()

    lines = candidate.splitlines()
    start_index = None
    for index, line in enumerate(lines):
        if re.match(r"^\s*def\s+\w+\s*\(", line):
            start_index = index
            break

    if start_index is None:
        return candidate.strip()

    import_lines = []
    for line in lines[:start_index]:
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            import_lines.append(line)

    code_lines = import_lines + ([""] if import_lines else []) + lines[start_index:]
    cleaned: list[str] = []
    for line in code_lines:
        if cleaned and not line.strip() and len(cleaned) > 0:
            cleaned.append(line)
            continue
        if cleaned and not line.startswith((" ", "\t")) and not re.match(r"^\s*(def|@)", line):
            break
        cleaned.append(line)

    return "\n".join(cleaned).strip()


def valid_function(code: str, name: str, description: str) -> bool:
    try:
        tree = ast.parse(code)
        found = next(node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name)
        match = re.search(r"Implement\s+" + re.escape(name) + r"\([^)]*\)", description)
        if not match or isinstance(found, ast.AsyncFunctionDef):
            return False
        expected = ast.parse("def " + match.group()[len("Implement "):] + ":\n    pass").body[0]
        args = found.args
        wanted = expected.args
        return ([a.arg for a in args.posonlyargs + args.args] ==
                [a.arg for a in wanted.posonlyargs + wanted.args] and
                len(args.defaults) == len(wanted.defaults) and not args.vararg and
                not args.kwarg and not args.kwonlyargs)
    except (SyntaxError, StopIteration, ValueError):
        return False


def build_task_prompt(
    task_description: str,
    function_name: str,
    visible_examples: list[str] | None = None,
) -> str:
    examples = "\n".join(f"- {example}" for example in (visible_examples or []))
    examples_block = f"\nVisible examples:\n{examples}\n" if examples else ""
    return (
        f"Task: {task_description}\n"
        f"Function name: {function_name}\n"
        f"{examples_block}"
        "Follow the required signature and error handling. "
        "Do not rely on hidden tests being visible."
    )
