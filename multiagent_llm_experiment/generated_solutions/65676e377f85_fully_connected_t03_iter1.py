def merge_intervals(intervals):
    if any(start > end for start, end in intervals):
        raise ValueError("Invalid interval")
        
    # Sort intervals based on start time
    intervals.sort()
    
    merged = []
    for current_start, current_end in intervals:
        if not merged:
            merged.append((current_start, current_end))
        else:
            last_start, last_end = merged[-1]
            if current_start <= last_end:
                merged[-1] = (last_start, max(last_end, current_end))
            else:
                merged.append((current_start, current_end))
    return merged
