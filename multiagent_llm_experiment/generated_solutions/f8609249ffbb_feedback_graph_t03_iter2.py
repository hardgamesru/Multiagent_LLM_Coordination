def merge_intervals(intervals):
    if any(start > end for start, end in intervals):
        raise ValueError("Invalid interval")
    
    # Sort intervals based on start time
    sorted_intervals = sorted(intervals)
    
    merged = []
    for current_interval in sorted_intervals:
        if not merged:
            merged.append(current_interval)
        else:
            last_start, last_end = merged[-1]
            curr_start, curr_end = current_interval
            
            if curr_start <= last_end + 1:  # Overlap or touch condition
                new_end = max(last_end, curr_end)
                merged[-1] = (last_start, new_end)
            else:
                merged.append(current_interval)
                
    return merged
