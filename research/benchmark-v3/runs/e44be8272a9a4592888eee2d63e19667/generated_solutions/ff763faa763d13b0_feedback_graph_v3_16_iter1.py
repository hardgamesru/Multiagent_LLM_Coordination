def weighted_schedule(jobs: list[list[int]]) -> int:
    jobs_copy = [list(j) for j in jobs]
    for s, e, v in jobs_copy:
        if not (s < e and v >= 0):
            raise ValueError
    if not jobs_copy:
        return 0
    jobs_sorted = sorted(jobs_copy, key=lambda x: x[1])
    ends = [e for _, e, _ in jobs_sorted]
    import bisect
    dp = [0] * (len(jobs_sorted) + 1)
    for i, (s, e, v) in enumerate(jobs_sorted, 1):
        j = bisect.bisect_right(ends, s, 0, i - 1)
        take = dp[j] + v
        skip = dp[i - 1]
        dp[i] = take if take > skip else skip
    return dp[-1]
