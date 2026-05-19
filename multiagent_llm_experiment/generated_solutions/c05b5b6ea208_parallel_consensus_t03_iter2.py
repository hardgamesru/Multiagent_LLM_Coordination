def merge_intervals(intervals):
    # Validate input intervals
    for start, end in intervals:
        if start > end:
            raise ValueError("Interval start must be less than or equal to end")
    
    # Sort intervals based on their start values
    sorted_intervals = sorted(intervals)
    
    merged = []
    for current_interval in sorted_intervals:
        # If no previous interval exists or no overlap with last interval
        if not merged or merged[-1][1] < current_interval[0]:
            merged.append(current_interval)
        else:
            # Extend the last interval's end point
            merged[-1] = (merged[-1][0], max(merged[-1][1], current_interval[1]))
    
    return merged
