def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    
    for query in queries:
        if not (0 <= query[0] <= query[1] < len(values)):
            raise ValueError("Invalid interval")
        
        # Handle empty or single element ranges with default value 0
        result.append(sum(values[query[0]:query[1]+1]))
    
    return result
