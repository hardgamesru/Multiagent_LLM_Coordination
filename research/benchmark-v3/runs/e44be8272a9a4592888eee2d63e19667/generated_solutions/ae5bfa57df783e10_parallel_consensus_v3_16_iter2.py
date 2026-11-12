def weighted_schedule(jobs: list[list[int]]) -> int:
    # Validate inputs without mutating
    for job in jobs:
        if len(job) != 3:
            raise ValueError
        s, e, v = job
        if not (isinstance(s, int) and isinstance(e, int) and isinstance(v, int)):
            raise ValueError
        if s >= e or v < 0:
            raise ValueError

    if not jobs:
        return 0

    # Sort by end time, keep original data intact
    sorted_jobs = sorted(jobs, key=lambda x: x[1])
    ends = [job[1] for job in sorted_jobs]
    n = len(sorted_jobs)

    # p[i]: index of last job before i that doesn't overlap (half-open, touching allowed)
    p = [-1] * n
    for i in range(n):
        s_i = sorted_jobs[i][0]
        lo, hi = 0, i - 1
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if ends[mid] <= s_i:
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        p[i] = ans

    # DP: dp[i] = best value using first i jobs (i from 0..n)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        incl = sorted_jobs[i - 1][2]
        if p[i - 1] != -1:
            incl += dp[p[i - 1] + 1]
        dp[i] = dp[i - 1] if dp[i - 1] > incl else incl

    return dp[n]
