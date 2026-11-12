def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        left, right = query
        
        # Проверка границ вне допустимого диапазона
        if left < 0 or right >= len(values):
            raise ValueError("Invalid interval")
            
        # Добавление суммы текущего интервала
        result.append(sum(values[left:right]))
    
    return result
