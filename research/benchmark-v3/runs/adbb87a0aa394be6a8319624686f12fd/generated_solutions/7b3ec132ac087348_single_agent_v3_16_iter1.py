def weighted_schedule(jobs):
    if not all(len(job) == 3 for job in jobs):
        raise ValueError("Each job must be a list of exactly three integers")
    
    valid_jobs = []
    for s, e, v in jobs:
        if not (isinstance(s, int) and isinstance(e, int) and isinstance(v, int)):
            raise ValueError("Job parameters must be integers")
        
        if s >= e or v < 0:
            continue
        
        valid_jobs.append((s, e, v))
    
    # Sort by end time first then by start time
    sorted_jobs = sorted(valid_jobs, key=lambda x: (x[1], x[0]))
    
    result = 0
    last_end = None
    
    for _, end, value in sorted_jobs:
        if last_end is None or end >= last_end:
            result += value
            last_end = end
            
    return result
