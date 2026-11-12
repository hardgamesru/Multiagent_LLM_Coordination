def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        start, end = min(query[0], query[1]), max(query[0], query[1])
        
        # Check validity of interval before proceeding
        if not (0 <= start < len(values) and 0 <= end <= len(values)):
            raise ValueError("Invalid interval")
            
        # Calculate sum for valid interval
        interval_sum = sum(values[start:end])
        result.append(interval_sum)
    
    return result
