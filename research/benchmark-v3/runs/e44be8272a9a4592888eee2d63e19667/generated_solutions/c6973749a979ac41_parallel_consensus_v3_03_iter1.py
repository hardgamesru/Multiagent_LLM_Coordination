def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        if not (0 <= query[0] <= query[1] <= len(values)):
            raise ValueError("Invalid interval")
        
        # Calculate inclusive range sum using slice with default stop value
        result.append(sum(values[query[0]:query[1]+1]))
    
    return result
