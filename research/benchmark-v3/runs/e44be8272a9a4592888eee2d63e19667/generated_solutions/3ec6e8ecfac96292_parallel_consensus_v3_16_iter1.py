def weighted_schedule(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        return 0
    
    valid_jobs = [(s, e, v) for s, e, v in jobs if s < e and v >= 0]
    
    if not valid_jobs:
        raise ValueError("No valid jobs found")
    
    # Sort by end time first then by start time
    sorted_jobs = sorted(valid_jobs, key=lambda x: (x[1], x[0]))
    
    result = []
    last_end_time = None
    
    for start, end, value in sorted_jobs:
        if last_end_time is None or last_end_time <= start:
            result.append(value)
            last_end_time = end
            
    return sum(result)
