def merge_intervals(intervals):
    # Check for invalid intervals
    for i in intervals:
        if i[0] > i[1]:
            raise ValueError("Interval start cannot be greater than end")
    
    # Handle edge case when no intervals provided
    if len(intervals) == 0:
        return []
        
    # Sort intervals based on the first element
    intervals.sort(key=lambda x: x[0])
    
    # Initialize result array with the first interval
    res = [intervals[0]]
    
    # Iterate through remaining intervals to check for overlap/adjacency
    for current_interval in intervals[1:]:
        last_merged = res[-1]
        
        # Check if current interval can be merged into previous one
        if current_interval[0] <= last_merged[1]:
            # Extend the last interval's end if necessary
            new_end = max(last_merged[1], current_interval[1])
            res[-1] = (last_merged[0], new_end)
        else:
            # No overlap; add this interval separately
            res.append(current_interval)
            
    return res
