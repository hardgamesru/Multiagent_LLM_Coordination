def weighted_schedule(jobs: list[list[int]]) -> int:
    from bisect import bisect_right

    jobs_copy = [list(j) for j in jobs]
    for s, e, v in jobs_copy:
        if s >= e or v < 0:
            raise ValueError

    if not jobs_copy:
        return 0

    jobs_sorted = sorted(jobs_copy, key=lambda x: x[1])
    ends = [e for _, e, _ in jobs_sorted]
    n = len(jobs_sorted)
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        s, e, v = jobs_sorted[i - 1]
        j = bisect_right(ends, s, hi=i - 1)
        dp[i] = max(dp[i - 1], dp[j] + v)

    return dp[n]
