from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    task_id: str
    name: str
    description: str
    function_name: str
    visible_examples: list[str]
    hidden_tests: str


def get_tasks() -> list[Task]:
    return [
        Task(
            task_id="t01",
            name="normalize_email",
            function_name="normalize_email",
            description=(
                "Implement normalize_email(email: str) -> str. Strip outer spaces. "
                "The email must contain exactly one @. Keep the local part case-sensitive. "
                "Lowercase the domain part. The domain must contain a dot. "
                "Local part and domain must be non-empty. Raise ValueError for invalid input."
            ),
            visible_examples=[
                'normalize_email("  User.Name@Example.COM  ") -> "User.Name@example.com"',
                'normalize_email("bad@@example.com") raises ValueError',
            ],
            hidden_tests="""
def expect_value_error(func, *args):
    try:
        func(*args)
        raise AssertionError("ValueError was not raised")
    except ValueError:
        pass

assert normalize_email("User@Example.COM") == "User@example.com"
assert normalize_email("  A.B+tag@Sub.Domain.ORG  ") == "A.B+tag@sub.domain.org"
assert normalize_email("CaseSensitive@DOMAIN.ru") == "CaseSensitive@domain.ru"
expect_value_error(normalize_email, "missing-at.example.com")
expect_value_error(normalize_email, "a@b@c.com")
expect_value_error(normalize_email, "@example.com")
expect_value_error(normalize_email, "local@")
expect_value_error(normalize_email, "local@example")
expect_value_error(normalize_email, "   ")
""",
        ),
        Task(
            task_id="t02",
            name="parse_csv_line",
            function_name="parse_csv_line",
            description=(
                "Implement parse_csv_line(line: str) -> list[str]. Use comma as separator. "
                "Fields may be enclosed in double quotes. Commas inside quoted fields are not separators. "
                "A double quote inside a quoted field is escaped as two double quotes. "
                "Return field values without outer quotes."
            ),
            visible_examples=[
                'parse_csv_line("a,b,c") -> ["a", "b", "c"]',
                'parse_csv_line("\\"a,b\\",c") -> ["a,b", "c"]',
            ],
            hidden_tests="""
assert parse_csv_line("a,b,c") == ["a", "b", "c"]
assert parse_csv_line('"a,b",c') == ["a,b", "c"]
assert parse_csv_line('"a""b",c') == ['a"b', "c"]
assert parse_csv_line('one,"two, too","three""3"') == ["one", "two, too", 'three"3']
assert parse_csv_line("a,,c,") == ["a", "", "c", ""]
assert parse_csv_line(',"",x') == ["", "", "x"]
assert parse_csv_line('  a ," b ",c ') == ["  a ", " b ", "c "]
assert parse_csv_line('"","comma, inside","quote "" inside"') == ["", "comma, inside", 'quote " inside']
assert parse_csv_line('"multi word",plain,"last"') == ["multi word", "plain", "last"]
""",
        ),
        Task(
            task_id="t03",
            name="merge_intervals",
            function_name="merge_intervals",
            description=(
                "Implement merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]. "
                "Merge overlapping intervals. Intervals may be unordered. If start > end, raise ValueError. "
                "Intervals touching at boundaries count as overlapping. Sort result by interval start."
            ),
            visible_examples=[
                "merge_intervals([(5, 7), (1, 3), (2, 4)]) -> [(1, 4), (5, 7)]",
                "merge_intervals([(1, 2), (2, 3)]) -> [(1, 3)]",
            ],
            hidden_tests="""
def expect_value_error(func, *args):
    try:
        func(*args)
        raise AssertionError("ValueError was not raised")
    except ValueError:
        pass

assert merge_intervals([]) == []
assert merge_intervals([(1, 3)]) == [(1, 3)]
assert merge_intervals([(5, 7), (1, 3), (2, 4)]) == [(1, 4), (5, 7)]
assert merge_intervals([(1, 2), (2, 3), (6, 8)]) == [(1, 3), (6, 8)]
assert merge_intervals([(-5, -1), (-3, 2), (10, 10)]) == [(-5, 2), (10, 10)]
assert merge_intervals([(4, 5), (1, 2), (2, 4)]) == [(1, 5)]
assert merge_intervals([(1, 10), (2, 3), (4, 8)]) == [(1, 10)]
expect_value_error(merge_intervals, [(3, 1)])
""",
        ),
        Task(
            task_id="t04",
            name="calculate_cart_total",
            function_name="calculate_cart_total",
            description=(
                "Implement calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float. "
                "Each item contains price, quantity, category. Price cannot be negative. Quantity must be positive. "
                "SALE10 gives 10 percent discount on the whole cart. FOOD5 gives 5 percent discount only "
                "on items with category equal to food. Unknown promo codes are ignored. Round total to 2 decimals. "
                "Raise ValueError for invalid item data."
            ),
            visible_examples=[
                "calculate_cart_total([{'price': 10, 'quantity': 2, 'category': 'book'}], 'SALE10') -> 18.0",
                "calculate_cart_total([{'price': 20, 'quantity': 1, 'category': 'food'}], 'FOOD5') -> 19.0",
            ],
            hidden_tests="""
def expect_value_error(func, *args):
    try:
        func(*args)
        raise AssertionError("ValueError was not raised")
    except ValueError:
        pass

assert calculate_cart_total([]) == 0.0
assert calculate_cart_total([{"price": 10, "quantity": 2, "category": "book"}]) == 20.0
assert calculate_cart_total([{"price": 10, "quantity": 2, "category": "book"}], "SALE10") == 18.0
assert calculate_cart_total([{"price": 20, "quantity": 1, "category": "food"}, {"price": 10, "quantity": 2, "category": "book"}], "FOOD5") == 39.0
assert calculate_cart_total([{"price": 0.1, "quantity": 3, "category": "food"}]) == 0.3
assert calculate_cart_total([{"price": 12.345, "quantity": 2, "category": "food"}], "FOOD5") == 23.46
assert calculate_cart_total([{"price": 5, "quantity": 2, "category": "food"}], "UNKNOWN") == 10.0
expect_value_error(calculate_cart_total, [{"price": -1, "quantity": 1, "category": "food"}])
expect_value_error(calculate_cart_total, [{"price": 1, "quantity": 0, "category": "food"}])
expect_value_error(calculate_cart_total, [{"price": 1, "category": "food"}])
""",
        ),
        Task(
            task_id="t05",
            name="top_k_frequent",
            function_name="top_k_frequent",
            description=(
                "Implement top_k_frequent(words: list[str], k: int) -> list[str]. Ignore word case. "
                "Return the k most frequent words. If frequencies are equal, sort words alphabetically. "
                "If k <= 0 return an empty list. If k is larger than the number of unique words, "
                "return all unique words in the correct order."
            ),
            visible_examples=[
                'top_k_frequent(["b", "A", "a", "b"], 2) -> ["a", "b"]',
                'top_k_frequent(["x", "y"], 5) -> ["x", "y"]',
            ],
            hidden_tests="""
assert top_k_frequent([], 3) == []
assert top_k_frequent(["Apple", "apple", "Banana"], 2) == ["apple", "banana"]
assert top_k_frequent(["b", "a", "c"], 3) == ["a", "b", "c"]
assert top_k_frequent(["x", "y", "x", "z", "y", "y"], 2) == ["y", "x"]
assert top_k_frequent(["Dog", "cat", "dog", "Cat", "bird"], 10) == ["cat", "dog", "bird"]
assert top_k_frequent(["a", "b"], 0) == []
assert top_k_frequent(["a", "b"], -1) == []
assert top_k_frequent(["b", "B", "a", "A", "c"], 2) == ["a", "b"]
assert top_k_frequent(["zz", "aa", "zz", "bb", "aa", "bb"], 2) == ["aa", "bb"]
""",
        ),
        Task(
            task_id="t06",
            name="detect_cycle",
            function_name="detect_cycle",
            description=(
                "Implement detect_cycle(dependencies: dict[str, list[str]]) -> bool. "
                "Detect whether a dependency graph contains a cycle. A dictionary key is a task. "
                "Its list values are tasks that the key depends on. Include nodes that appear only in values. "
                "An empty graph has no cycle."
            ),
            visible_examples=[
                'detect_cycle({"build": ["compile"], "compile": []}) -> False',
                'detect_cycle({"a": ["b"], "b": ["a"]}) -> True',
            ],
            hidden_tests="""
assert detect_cycle({}) is False
assert detect_cycle({"build": ["compile"], "compile": ["lint"], "lint": []}) is False
assert detect_cycle({"a": ["b"], "b": ["c"], "c": ["a"]}) is True
assert detect_cycle({"a": ["a"]}) is True
assert detect_cycle({"a": ["b"], "b": [], "c": ["d"], "d": ["c"]}) is True
assert detect_cycle({"deploy": ["build"], "test": ["build"]}) is False
assert detect_cycle({"a": ["b"], "b": ["c"], "c": [], "d": ["e"], "e": []}) is False
assert detect_cycle({"a": ["b"], "b": ["c"], "c": ["b"]}) is True
assert detect_cycle({"a": ["missing"]}) is False
""",
        ),
        Task(
            task_id="t07",
            name="analyze_logs",
            function_name="analyze_logs",
            description=(
                "Implement analyze_logs(lines: list[str]) -> dict. Valid line format is "
                "YYYY-MM-DD HH:MM:SS LEVEL ENDPOINT STATUS. LEVEL is INFO, WARNING, or ERROR. "
                "STATUS must be a three-digit HTTP status code. "
                "Ignore invalid lines. Return {'total': valid_count, 'by_level': counts_by_level, "
                "'errors': number_of_error_lines, 'most_common_endpoint': endpoint_or_None}. "
                "If endpoint frequencies tie, choose lexicographically smallest endpoint."
            ),
            visible_examples=[
                'analyze_logs(["2026-05-19 12:30:01 INFO /api/users 200"]) -> total 1',
                'analyze_logs(["bad line"]) -> most_common_endpoint None',
            ],
            hidden_tests="""
result = analyze_logs([])
assert result == {"total": 0, "by_level": {}, "errors": 0, "most_common_endpoint": None}

lines = [
    "2026-05-19 12:30:01 INFO /api/users 200",
    "2026-05-19 12:30:02 ERROR /api/users 500",
    "bad line",
    "2026-05-19 12:30:03 WARNING /api/orders 404",
]
assert analyze_logs(lines) == {"total": 3, "by_level": {"INFO": 1, "ERROR": 1, "WARNING": 1}, "errors": 1, "most_common_endpoint": "/api/users"}

assert analyze_logs(["2026-05-19 12:30:01 DEBUG /x 200"])["total"] == 0
assert analyze_logs(["2026/05/19 12:30:01 INFO /x 200"])["total"] == 0
assert analyze_logs(["2026-05-19 12:30:01 INFO /b 200", "2026-05-19 12:30:02 INFO /a 200"])["most_common_endpoint"] == "/a"
assert analyze_logs(["2026-05-19 12:30:01 ERROR /x 500", "2026-05-19 12:30:02 ERROR /x 503"])["errors"] == 2
assert analyze_logs(["2026-05-19 12:30:01 INFO /x twohundred"])["total"] == 0
assert analyze_logs(["2026-05-19 12:30:01 WARNING /x 200 extra"])["total"] == 0
assert analyze_logs(["2026-05-19 12:30:01 INFO /z 200", "2026-05-19 12:30:02 INFO /a 200", "2026-05-19 12:30:03 INFO /z 201"])["most_common_endpoint"] == "/z"
""",
        ),
        Task(
            task_id="t08",
            name="group_by_category",
            function_name="group_by_category",
            description=(
                "Implement group_by_category(items: list[dict]) -> dict[str, list[dict]]. "
                "Group items by the category field. If an item has no category, use 'unknown'. "
                "Preserve the original order of items inside each category. Return a dictionary "
                "whose keys are categories and values are lists of items in that category."
            ),
            visible_examples=[
                "group_by_category([{'name': 'a', 'category': 'x'}, {'name': 'b'}]) -> {'x': [...], 'unknown': [...]}",
                "group_by_category([]) -> {}",
            ],
            hidden_tests="""
items = [{"id": 1, "category": "food"}, {"id": 2, "category": "book"}, {"id": 3, "category": "food"}]
result = group_by_category(items)
assert list(result.keys()) == ["food", "book"]
assert [item["id"] for item in result["food"]] == [1, 3]
assert [item["id"] for item in result["book"]] == [2]
assert group_by_category([]) == {}
assert list(group_by_category([{"id": 1}, {"id": 2, "category": "x"}]).keys()) == ["unknown", "x"]
assert [item["id"] for item in group_by_category([{"id": 1}, {"id": 2}])["unknown"]] == [1, 2]
assert group_by_category([{"id": 1, "category": ""}]) == {"": [{"id": 1, "category": ""}]}
original = {"id": 10, "category": "tools"}
assert group_by_category([original])["tools"][0] is original
mixed = [{"id": "a", "category": "x"}, {"id": "b", "category": "x"}, {"id": "c"}]
assert [item["id"] for item in group_by_category(mixed)["x"]] == ["a", "b"]
""",
        ),
        Task(
            task_id="t09",
            name="resolve_build_order",
            function_name="resolve_build_order",
            description=(
                "Implement resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]. "
                "Return a deterministic installation/build order for tasks. A key depends on all tasks "
                "listed in its value. Every dependency must appear before the task that depends on it. "
                "Include nodes that appear only in dependency lists. If several nodes are currently available, "
                "choose them in lexicographic order. Raise ValueError if the graph contains a cycle."
            ),
            visible_examples=[
                'resolve_build_order({"app": ["lib"], "lib": []}) -> ["lib", "app"]',
                'resolve_build_order({"a": ["b"], "b": ["a"]}) raises ValueError',
            ],
            hidden_tests="""
def expect_value_error(func, *args):
    try:
        func(*args)
        raise AssertionError("ValueError was not raised")
    except ValueError:
        pass

assert resolve_build_order({}) == []
assert resolve_build_order({"app": ["lib"], "lib": []}) == ["lib", "app"]
assert resolve_build_order({"app": ["core", "ui"], "ui": ["core"]}) == ["core", "ui", "app"]
assert resolve_build_order({"b": [], "a": []}) == ["a", "b"]
assert resolve_build_order({"deploy": ["build"], "test": ["build"]}) == ["build", "deploy", "test"]
assert resolve_build_order({"a": ["c"], "b": ["c"], "c": []}) == ["c", "a", "b"]
assert resolve_build_order({"package": ["compile", "test"], "test": ["compile"], "compile": ["lint"]}) == ["lint", "compile", "test", "package"]
expect_value_error(resolve_build_order, {"a": ["b"], "b": ["a"]})
expect_value_error(resolve_build_order, {"a": ["a"]})
""",
        ),
    ]
