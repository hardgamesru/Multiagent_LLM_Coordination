def weighted_schedule(jobs: list[list[int]]) -> int:
    import bisect
    jobs_sorted = sorted((s, e, v) for s, e, v in jobs)
    for s, e, v in jobs_sorted:
        if not (s < e and v >= 0):
            raise ValueError
    n = len(jobs_sorted)
    if n == 0:
        return 0
    starts = [s for s, _, _ in jobs_sorted]
    ends = [e for _, e, _ in jobs_sorted]
    p = [0] * n
    for i in range(n):
        j = bisect.bisect_right(ends, starts[i]) - 1
        p[i] = j
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        s, e, v = jobs_sorted[i - 1]
        dp[i] = max(dp[i - 1], v + dp[p[i - 1] + 1])
    return dp[n]
