def weighted_schedule(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        return 0
    
    # Проверка корректности входных данных
    for job in jobs:
        start, end, value = job
        if start >= end or value < 0:
            raise ValueError("Invalid job parameters")
    
    # Сортировка по началу интервала
    sorted_jobs = sorted(jobs, key=lambda x: x[0])
    
    dp = [0] * len(sorted_jobs)
    
    for i in range(len(sorted_jobs)):
        current_start, current_end, _ = sorted_jobs[i]
        
        # Инициализация текущего максимального результата
        max_value = 0
        
        # Поиск предыдущих не пересекающихся задач
        for j in range(i):
            prev_start, prev_end, _ = sorted_jobs[j]
            
            # Совместимость: текущая задача не перекрывает предыдущую
            if current_start >= prev_end:
                max_value = max(max_value, dp[j])
        
        # Обновление динамического массива
        dp[i] = max_value + sorted_jobs[i][2]
    
    return max(dp, default=0)
