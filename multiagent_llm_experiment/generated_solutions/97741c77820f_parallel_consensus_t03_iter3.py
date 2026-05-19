def merge_intervals(intervals):
    # Validate intervals
    for i in intervals:
        if len(i) != 2 or i[0] > i[1]:
            raise ValueError("Invalid interval")
    
    # Handle edge case of no intervals
    if not intervals:
        return []
    
    # Sort intervals based on start time
    intervals.sort(key=lambda x: x[0])
    
    # Initialize result array with first interval
    result = [intervals[0]]
    
    # Iterate through remaining intervals to merge overlaps
    for current_interval in intervals[1:]:
        last_merged = result[-1]
        
        # Check if current interval can be merged into previous one
        if current_interval[0] <= last_merged[1]:
            # Extend the end of the previous interval
            result[-1] = (last_merged[0], max(last_merged[1], current_interval[1]))
        else:
            # Add new interval since it doesn't overlap
            result.append(current_interval)
            
    return result
