def weighted_schedule(jobs):
    jobs_copy = [list(j) for j in jobs]
    for s, e, v in jobs_copy:
        if not (s < e and v >= 0):
            raise ValueError
    sorted_jobs = sorted(jobs_copy, key=lambda x: x[1])
    ends = [e for _, e, _ in sorted_jobs]
    n = len(sorted_jobs)
    dp = [0] * (n + 1)
    import bisect
    for i in range(1, n + 1):
        s, e, v = sorted_jobs[i - 1]
        j = bisect.bisect_right(ends, s, 0, i - 1)
        dp[i] = max(dp[i - 1], dp[j] + v)
    return dp[n]
