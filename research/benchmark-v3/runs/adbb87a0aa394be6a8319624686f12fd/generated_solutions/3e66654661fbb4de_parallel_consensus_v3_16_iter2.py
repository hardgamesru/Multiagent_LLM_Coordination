def weighted_schedule(jobs):
    # Validate input without mutating
    for job in jobs:
        if not (isinstance(job, list) and len(job) == 3):
            raise ValueError
        start, end, value = job
        if not (isinstance(start, int) and isinstance(end, int) and isinstance(value, int)):
            raise ValueError
        if not (start < end and value >= 0):
            raise ValueError

    if not jobs:
        return 0

    # Sort by end time
    sorted_jobs = sorted(jobs, key=lambda j: j[1])
    ends = [job[1] for job in sorted_jobs]
    n = len(sorted_jobs)

    # p[i] = index of last job compatible with i (or -1)
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
        dp[i] = incl if incl > dp[i - 1] else dp[i - 1]

    return dp[n]
