def merge_intervals(intervals):
    # Validate input intervals
    for i in intervals:
        if len(i) != 2 or i[0] > i[1]:
            raise ValueError("Invalid interval")
    
    # Sort intervals based on their start value
    sorted_intervals = sorted(intervals)
    
    merged = []
    for current_interval in sorted_intervals:
        # If the list of merged intervals is empty 
        # or if the current interval does not overlap with the previous one,
        # simply append it to the list
        if not merged or merged[-1][1] < current_interval[0]:
            merged.append(current_interval)
        else:
            # Otherwise, there is an overlap, so we merge the current and previous intervals
            prev_start, prev_end = merged.pop()
            new_end = max(prev_end, current_interval[1])
            merged.append((prev_start, new_end))
            
    return merged
