def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            # Skip zero-length or reversed intervals
            if len(interval) != 2 or interval[0] >= interval[1]:
                continue
            
            # Merge with previous interval if possible
            if result and interval[0] <= result[-1][1]:
                result[-1][1] = max(result[-1][1], interval[1])
            else:
                result.append(list(interval))
        
        return result
    
    # Validate no reversed intervals
    for interval in base + cuts:
        if interval[0] > interval[1]:
            raise ValueError("Interval is reversed")
    
    # Combine all intervals into one set
    combined_base = [(interval[0], interval[1]) for interval in base]
    combined_cuts = [(interval[0], interval[1]) for interval in cuts]
    
    # Subtract cuts from base using two pointers technique
    merged_base = merge_intervals(combined_base)
    merged_cuts = merge_intervals(combined_cuts)
    
    result = []
    i = j = 0
    
    while i < len(merged_base) and j < len(merged_cuts):
        if merged_base[i][0] < merged_cuts[j][0]:
            # Expand current interval until it overlaps cut
            start = merged_base[i][0]
            while i < len(merged_base) and \
                  merged_base[i][0] < merged_cuts[j][1]:
                i += 1
            # Add remaining part of original interval
            result.append([start, merged_base[i-1][1]])
        elif merged_cuts[j][0] < merged_base[i][0]:
            # Move to next cut interval
            j += 1
        else:
            # Overlapping intervals, skip both
            i += 1
            j += 1
    
    # Add remaining intervals from base
    while i < len(merged_base):
        result.append(merged_base[i])
        i += 1
    
    return result
