def weighted_schedule(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        return 0
    
    valid_jobs = [(s,e,v) for s,e,v in jobs if s<e and v>=0]
    
    # Sort by finish time
    sorted_jobs = sorted(valid_jobs, key=lambda x:x[1])
    
    current_end = None
    total_value = 0
    
    for start, end, value in sorted_jobs:
        if current_end is None or current_end <= start:
            total_value += value
            current_end = end
            
    return total_value
