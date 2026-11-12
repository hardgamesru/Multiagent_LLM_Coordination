def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        if not (0 <= query[0] <= query[1] <= len(values)):
            raise ValueError("Invalid interval")
        
        # Handle empty interval case
        start, end = min(query), max(query)
        result.append(sum(values[start:end]))
    
    return result
