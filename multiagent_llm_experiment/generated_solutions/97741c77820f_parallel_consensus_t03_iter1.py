def merge_intervals(intervals):
    # Check for invalid intervals
    for start, end in intervals:
        if start > end:
            raise ValueError("Interval start cannot be greater than end")
    
    # Handle edge case of no intervals
    if len(intervals) == 0:
        return []
        
    # Sort intervals based on start time
    intervals.sort(key=lambda x: x[0])
    
    # Initialize merged intervals array
    merged = [list(intervals[0])]  # Convert first interval to mutable list
    
    # Iterate through remaining intervals
    for current_start, current_end in intervals[1:]:
        last_merged = merged[-1]
        
        # If current interval overlaps with previous one, merge them
        if current_start <= last_merged[1]:  
            last_merged[1] = max(last_merged[1], current_end)
        else:
            # Otherwise add new interval
            merged.append([current_start, current_end])
            
    # Return as immutable tuples
    return [tuple(interval) for interval in merged]
