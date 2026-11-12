def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        if not (0 <= query[0] <= query[1] <= len(values)):
            raise ValueError("Invalid interval")
        
        # Для пустых интервалов сумма равна 0
        start, end = query[0], query[1]+1  
        result.append(sum(values[start:end]))
    
    return result
