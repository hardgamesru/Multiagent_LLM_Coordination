def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        left, right = query
        
        if not (0 <= left <= right <= len(values)):
            raise ValueError("Invalid interval")
            
        # Handle empty or single element ranges with sum 0
        result.append(sum(values[left:right]))
    
    return result
