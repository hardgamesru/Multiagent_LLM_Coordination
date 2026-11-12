def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    n = len(values)
    for q in queries:
        if len(q) != 2:
            raise ValueError
        left, right = q
        if not (0 <= left <= right <= n):
            raise ValueError
    return [sum(values[left:right]) for left, right in queries]
