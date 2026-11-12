def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        if not (0 <= query[0] <= query[1] < len(values)):
            raise ValueError("Invalid interval")
        
        # Handle empty interval case
        start, end = max(query[0], 0), min(query[1]+1, len(values))
        result.append(sum(values[start:end]))
    
    return result
