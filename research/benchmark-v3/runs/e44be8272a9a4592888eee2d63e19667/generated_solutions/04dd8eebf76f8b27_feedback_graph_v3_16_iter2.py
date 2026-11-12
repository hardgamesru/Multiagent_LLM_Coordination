def weighted_schedule(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        return 0
    
    # Проверка корректности входных данных
    for job in jobs:
        start, end, val = job
        if start >= end or val < 0:
            raise ValueError("Invalid job parameters")
    
    # Сортировка по концу интервала
    sorted_jobs = sorted(jobs, key=lambda x: x[1])
    
    result = []
    current_end = None
    
    for job in sorted_jobs:
        start, end, value = job
        
        # Добавляем первое задание или выбираем не пересекающееся
        if len(result) == 0 or current_end is None or end >= current_end:
            result.append(value)
            current_end = end
            
    return sum(result)
