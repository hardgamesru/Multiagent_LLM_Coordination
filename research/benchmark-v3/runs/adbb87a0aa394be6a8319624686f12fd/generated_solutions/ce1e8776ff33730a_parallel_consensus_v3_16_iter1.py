from typing import List

def weighted_schedule(jobs: List[List[int]]) -> int:
    if not jobs:
        return 0
    
    # Validate each job
    for j in jobs:
        start, end, val = j
        if start >= end or val < 0:
            raise ValueError("Invalid job parameters")
    
    # Sort jobs by end time
    sorted_jobs = sorted(jobs, key=lambda x: x[1])
    
    max_values = []
    current_end = float('-inf')
    
    for job in sorted_jobs:
        start, end, value = job
        
        # If new job starts after previous one ends, it's compatible
        if start >= current_end:
            max_values.append(value)
            current_end = end
            
    return sum(max_values)
