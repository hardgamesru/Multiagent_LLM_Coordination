def merge_intervals(intervals):
    # Check for invalid intervals
    if any(start > end for start, end in intervals):
        raise ValueError("Invalid interval found")
    
    # Handle edge case of no intervals
    if len(intervals) <= 1:
        return intervals[:]
    
    # Sort intervals based on start time
    intervals.sort()
    
    # Initialize merged intervals with first interval
    merged = [list(intervals[0])]  
    
    for current_start, current_end in intervals[1:]:
        last_merged_start, last_merged_end = merged[-1]
        
        # Overlap check: current interval overlaps with previous one
        if current_start <= last_merged_end + 1:
            # Merge intervals by updating the end to max value
            merged[-1][1] = max(last_merged_end, current_end)
        else:
            # No overlap; add new interval
            merged.append([current_start, current_end])
            
    # Convert back to tuples before returning
    return [tuple(interval) for interval in merged]
