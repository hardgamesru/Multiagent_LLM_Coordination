def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    n = len(values)
    for q in queries:
        if not (isinstance(q, list) and len(q) == 2):
            raise ValueError
        left, right = q
        if not (isinstance(left, int) and isinstance(right, int)):
            raise ValueError
        if not (0 <= left <= right <= n):
            raise ValueError
    prefix = [0] * (n + 1)
    for i, v in enumerate(values, 1):
        prefix[i] = prefix[i - 1] + v
    return [prefix[r] - prefix[l] for l, r in queries]
