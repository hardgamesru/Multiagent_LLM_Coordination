def weighted_schedule(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        return 0
    
    valid_jobs = [(s,e,v) for s,e,v in jobs if s < e and v >= 0]
    
    if not valid_jobs:
        raise ValueError("Invalid jobs provided")
    
    # Sort by end time first then by start time
    sorted_jobs = sorted(valid_jobs, key=lambda x: (x[1], x[0]))
    
    max_values = []
    current_end = None
    
    for job in sorted_jobs:
        start, end, value = job
        
        # Check compatibility: no overlap except touching endpoints
        if (current_end is None or 
            (current_end == start and len(max_values)) or 
            (end > current_end)):
            
            max_values.append(value)
            current_end = end
    
    return sum(max_values)
