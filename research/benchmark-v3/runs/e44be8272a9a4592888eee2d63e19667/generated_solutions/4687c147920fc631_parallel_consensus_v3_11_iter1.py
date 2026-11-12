def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            if not result or interval[0] > result[-1][1]:
                # No overlap, add new interval
                result.append(interval[:])
            else:
                # Merge with previous interval
                prev_end = result[-1][1]
                result[-1][1] = max(prev_end, interval[1])
        return result
    
    # Combine base and cuts into one set of intervals
    combined = base + cuts
    
    # Sort intervals by start point
    combined.sort()
    
    # Remove empty intervals
    filtered = [(s,e) for s,e in combined if e > s]
    
    # Find gaps between intervals
    gaps = []
    for i in range(len(filtered)-1):
        next_start = filtered[i+1][0]
        current_end = filtered[i][1]
        if next_start != current_end:
            gaps.append([current_end, next_start])
    
    # Merge adjacent gaps
    merged_gaps = merge_intervals(gaps)
    
    # Convert negative length intervals to empty
    final_result = [(s,e) for s,e in merged_gaps if e > s]
    
    return final_result
