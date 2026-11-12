def weighted_schedule(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        raise ValueError("Invalid job format")
    
    # Фильтруем некорректные входные данные
    valid_jobs = [(s, e, v) for s, e, v in jobs if s < e and v >= 0]
    
    # Сортируем по концу интервала
    sorted_jobs = sorted(valid_jobs, key=lambda x: x[1])
    
    result = []
    current_end = None
    
    # Алгоритм жадного выбора
    for start, end, value in sorted_jobs:
        if current_end is None or current_end <= start:
            result.append((end, value))
            current_end = end
    
    return sum(v for _, v in result)
