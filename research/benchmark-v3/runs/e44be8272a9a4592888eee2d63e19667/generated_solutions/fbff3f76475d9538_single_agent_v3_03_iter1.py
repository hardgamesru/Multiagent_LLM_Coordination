def range_sums(values: list[int], queries: list[list[int]]) -> list[int]:
    result = []
    for q in queries:
        if not (0 <= q[0] <= q[1] <= len(values)):
            raise ValueError("Invalid query interval")
        
        # Handle empty interval case
        start = max(q[0], 0)
        end = min(q[1]+1, len(values))
        total = sum(values[start:end])
        result.append(total)
    
    return result
