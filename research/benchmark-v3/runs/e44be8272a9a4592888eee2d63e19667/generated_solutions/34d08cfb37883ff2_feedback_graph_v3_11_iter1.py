def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for start, end in intervals:
            if not result or result[-1][1] < start:
                result.append([start, end])
            else:
                # Merge overlapping intervals
                result[-1][1] = max(result[-1][1], end)
        return result

    def check_validity(interval):
        if interval[0] >= interval[1]:
            raise ValueError("Invalid interval")
    
    # Validate reversed intervals
    for interval in base + cuts:
        check_validity(interval)
    
    # Remove zero-length intervals
    base = [(s,e) for s,e in base if e-s > 0]
    cuts = [(s,e) for s,e in cuts if e-s > 0]
    
    # Sort intervals by start time
    base.sort()
    cuts.sort()
    
    # Find difference of intervals
    diff = []
    i = j = 0
    while i < len(base):
        while j < len(cuts) and cuts[j][0] < base[i][1]:
            # If cut ends before current base starts, skip it
            if cuts[j][1] <= base[i][0]:
                j += 1
                continue
            # Subtract overlapping part
            elif cuts[j][0] >= base[i][0]:
                base_start = max(cuts[j][0], base[i][0])
                base_end = min(cuts[j][1], base[i][1])
                if base_end > base_start:
                    diff.append([base_start, base_end])
                # Move past fully covered base interval
                i += 1
                break
            else:
                # Cut covers entire base interval
                i += 1
                j += 1
                continue
        
        # Add remaining uncut base intervals
        if i < len(base):
            diff.append(base[i])
            i += 1
            
    return merge_intervals(diff)
