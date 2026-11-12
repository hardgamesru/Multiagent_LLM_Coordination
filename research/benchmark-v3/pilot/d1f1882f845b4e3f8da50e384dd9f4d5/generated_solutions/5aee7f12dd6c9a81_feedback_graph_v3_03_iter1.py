def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        left, right = query
        
        # Validate indices and handle empty interval
        if not (0 <= left <= right <= len(values)):
            raise ValueError("Invalid range")
            
        # Sum elements from left to right inclusive
        total = sum(values[left:right+1])
        result.append(total)
    
    return result
