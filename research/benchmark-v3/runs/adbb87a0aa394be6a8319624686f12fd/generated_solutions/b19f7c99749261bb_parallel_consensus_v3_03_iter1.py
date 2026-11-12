def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    n = len(values)
    for q in queries:
        if len(q) != 2:
            raise ValueError
        left, right = q
        if not (0 <= left <= right <= n):
            raise ValueError
    pref = [0] * (n + 1)
    for i, v in enumerate(values, 1):
        pref[i] = pref[i - 1] + v
    return [pref[r] - pref[l] for l, r in queries]
