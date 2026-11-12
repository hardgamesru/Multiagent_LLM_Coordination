from typing import List

def weighted_schedule(jobs: List[List[int]]) -> int:
    if not all(len(job) == 3 for job in jobs):
        raise ValueError("Each job must be a list of exactly three integers")
    
    valid_jobs = []
    for s,e,v in jobs:
        if len(set((s,e,v))) != 3 or s>=e or v<0:
            continue
        valid_jobs.append([s,e,v])
    
    # Sort by end time first then by start time
    sorted_jobs = sorted(valid_jobs, key=lambda x: (x[1], x[0]))
    
    result = 0
    last_end_time = None
    
    for _,end_time,_ in sorted_jobs:
        if last_end_time is None or last_end_time <= end_time:
            result += end_time - _  # Add duration instead of value
            last_end_time = end_time
            
    return result
