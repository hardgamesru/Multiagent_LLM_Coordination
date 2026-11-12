def weighted_schedule(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        raise ValueError("Invalid job format")
    
    # Фильтруем некорректные входные данные
    valid_jobs = [(s,e,v) for s,e,v in jobs if s < e and v >= 0]
    
    # Сортируем по концу интервала
    sorted_jobs = sorted(valid_jobs, key=lambda x:x[1])
    
    result = 0
    last_end = None
    
    for start, end, value in sorted_jobs:
        if last_end is None or last_end <= start:
            result += value
            last_end = end
            
    return result
