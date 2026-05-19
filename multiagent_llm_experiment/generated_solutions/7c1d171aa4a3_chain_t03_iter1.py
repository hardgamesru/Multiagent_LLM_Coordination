def merge_intervals(intervals):
    # Validate input
    for start, end in intervals:
        if start > end:
            raise ValueError("Invalid interval")
    
    # Sort intervals by their start values
    sorted_intervals = sorted(intervals)
    
    # Initialize result with first interval
    merged = [sorted_intervals[0]] if sorted_intervals else []
    
    # Iterate through remaining intervals to merge overlaps
    for current_start, current_end in sorted_intervals[1:]:
        last_merged_start, last_merged_end = merged[-1]
        
        # Check overlap/adjacency condition
        if current_start <= last_merged_end + 1:
            # Extend previous interval
            merged[-1] = (last_merged_start, max(last_merged_end, current_end))
        else:
            # Add new non-overlapping interval
            merged.append((current_start, current_end))
            
    return merged
