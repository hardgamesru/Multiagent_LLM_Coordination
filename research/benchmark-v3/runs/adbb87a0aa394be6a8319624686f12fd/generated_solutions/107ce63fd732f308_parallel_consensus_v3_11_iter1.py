def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            if not result or interval[0] > result[-1][1]:
                # No overlap, add new interval
                result.append(interval)
            else:
                # Merge with previous interval
                prev_end = result[-1][1]
                result[-1][1] = max(prev_end, interval[1])
        return result

    # Combine base and cuts into one set of intervals
    combined = base + cuts
    
    # Sort intervals by start point
    combined.sort()
    
    # Remove empty intervals and reverse direction errors
    valid_intervals = [(s,e) for s,e in combined if s < e]
    
    # Find gaps between intervals after removing cuts
    gaps = []
    for i in range(len(valid_intervals)):
        if i == 0:
            # First interval
            gaps.append([None, valid_intervals[i][0]])
        gaps.append(valid_intervals[i])
    
    # Skip last gap since it's always present
    gaps = gaps[:-1]
    
    # Calculate actual gaps after subtraction
    final_gaps = []
    for g in gaps:
        if g[0] is None:
            # Start from negative infinity
            start = float('-inf')
        else:
            start = g[1]
        
        try:
            next_start = gaps[gaps.index(g)+1][0]
        except IndexError:
            # Last interval's end
            next_start = float('inf')
            
        # Add valid gap
        if start != next_start:
            final_gaps.append([start, min(next_start, valid_intervals[-1][1])])
    
    # Merge adjacent gaps that touch
    return merge_intervals(final_gaps)
