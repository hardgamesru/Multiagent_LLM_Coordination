def weighted_schedule(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        return 0
    
    valid_jobs = []
    for s, e, v in jobs:
        if s >= e or v < 0:
            raise ValueError("Invalid job parameters")
        valid_jobs.append((s, e, v))
    
    # Sort by end time first then by start time
    sorted_jobs = sorted(valid_jobs, key=lambda x: (x[1], x[0]))
    
    result = 0
    last_end_time = None
    
    for _, end_time, value in sorted_jobs:
        if last_end_time is None or last_end_time <= end_time:
            result += value
            last_end_time = end_time
            
    return result
