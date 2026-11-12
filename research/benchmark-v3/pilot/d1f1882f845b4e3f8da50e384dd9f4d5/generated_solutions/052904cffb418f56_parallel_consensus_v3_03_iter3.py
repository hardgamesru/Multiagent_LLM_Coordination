def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        left, right = query
        
        if not (0 <= left <= right < len(values)):
            raise ValueError("Invalid interval")
            
        # Calculate inclusive range sum using slice with default stop value
        total = sum(values[left:right+1])
        result.append(total)
    
    return result
