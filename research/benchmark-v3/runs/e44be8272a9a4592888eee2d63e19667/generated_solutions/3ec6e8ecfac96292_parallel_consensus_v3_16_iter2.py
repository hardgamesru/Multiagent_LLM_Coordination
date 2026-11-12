def weighted_schedule(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        return 0
    
    valid_jobs = [(s, e, v) for s,e,v in jobs if s < e and v >= 0]
    
    # Sort by end time first then by start time
    sorted_jobs = sorted(valid_jobs, key=lambda x: (x[1], x[0]))
    
    result = []
    last_end = None
    
    for start, end, value in sorted_jobs:
        if last_end is None or last_end <= start:
            result.append(value)
            last_end = end
            
    return sum(result)
