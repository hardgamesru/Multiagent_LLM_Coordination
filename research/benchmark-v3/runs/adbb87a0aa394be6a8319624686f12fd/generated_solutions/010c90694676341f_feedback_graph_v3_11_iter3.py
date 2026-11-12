def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            # Skip empty or reversed intervals
            if len(interval) != 2 or interval[0] >= interval[1]:
                continue
            
            # Merge overlapping intervals
            if not result or result[-1][1] < interval[0]:
                result.append(interval)
            else:
                result[-1][1] = max(result[-1][1], interval[1])
        
        return result

    # Convert to sorted lists of intervals
    base_intervals = [(b[0], b[1]) for b in base if len(b) == 2 and b[0] < b[1]]
    cut_intervals = [(c[0], c[1]) for c in cuts if len(c) == 2 and c[0] < c[1]]
    
    # Subtract cut intervals from base intervals
    remaining_intervals = []
    i = j = 0
    while i < len(base_intervals) and j < len(cut_intervals):
        bi_start, bi_end = base_intervals[i]
        ci_start, ci_end = cut_intervals[j]
        
        # Check if current base interval is fully contained in a cut interval
        if bi_start >= ci_start and bi_end <= ci_end:
            i += 1
            continue
        
        # Find intersection with cut interval
        start = max(bi_start, ci_start)
        end = min(bi_end, ci_end)
        
        # If there's no intersection, move to next base interval
        if start >= end:
            remaining_intervals.append([bi_start, bi_end])
            i += 1
            continue
        
        # Remove completely covered parts of base interval
        if bi_start < ci_start:
            remaining_intervals.append([bi_start, ci_start])
        elif bi_end > ci_end:
            remaining_intervals.append([ci_end, bi_end])
        
        # Move to next cut interval
        j += 1
    
    # Add remaining uncut base intervals
    while i < len(base_intervals):
        remaining_intervals.append(base_intervals[i])
        i += 1
    
    # Merge adjacent intervals
    return merge_intervals(remaining_intervals)
