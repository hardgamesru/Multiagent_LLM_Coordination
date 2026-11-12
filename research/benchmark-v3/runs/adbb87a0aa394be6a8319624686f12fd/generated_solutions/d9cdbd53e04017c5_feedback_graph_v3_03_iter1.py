def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        left, right = query
        
        # Проверка границ интервалов
        if not (0 <= left <= right <= len(values)):
            raise ValueError("Invalid interval")
            
        # Для пустого интервала суммируем 0
        result.append(sum(values[left:right]))
    
    return result
