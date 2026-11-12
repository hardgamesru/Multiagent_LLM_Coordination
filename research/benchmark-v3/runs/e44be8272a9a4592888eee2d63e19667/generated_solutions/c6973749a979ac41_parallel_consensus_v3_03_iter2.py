def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        if not (0 <= query[0] <= len(values) and 0 <= query[1] <= len(values)):
            raise ValueError("Invalid interval")
        
        # Handle empty interval case
        start, end = min(query[0], query[1]), max(query[0], query[1])
        interval_sum = sum(values[start:end])
        result.append(interval_sum)
    
    return result
