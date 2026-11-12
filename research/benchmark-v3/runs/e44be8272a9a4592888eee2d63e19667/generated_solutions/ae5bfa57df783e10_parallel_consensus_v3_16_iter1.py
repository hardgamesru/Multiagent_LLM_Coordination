def weighted_schedule(jobs: list[list[int]]) -> int:
    for j in jobs:
        if not (isinstance(j, list) and len(j) == 3):
            raise ValueError
        s, e, v = j
        if not (isinstance(s, int) and isinstance(e, int) and isinstance(v, int)):
            raise ValueError
        if s >= e or v < 0:
            raise ValueError

    if not jobs:
        return 0

    jobs_sorted = sorted(jobs, key=lambda x: x[1])
    ends = [e for _, e, _ in jobs_sorted]

    import bisect
    n = len(jobs_sorted)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        s, e, v = jobs_sorted[i - 1]
        j = bisect.bisect_right(ends, s, 0, i - 1)
        dp[i] = max(dp[i - 1], dp[j] + v)
    return dp[n]
