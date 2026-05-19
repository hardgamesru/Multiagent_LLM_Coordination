def merge_intervals(intervals):
    # Validate input intervals and sort them based on their starting point
    sorted_intervals = []
    for interval in intervals:
        if len(interval) != 2 or interval[0] > interval[1]:
            raise ValueError("Invalid interval")
        sorted_intervals.append((interval[0], interval[1]))
    sorted_intervals.sort()
    
    merged = []
    for current_interval in sorted_intervals:
        # If no previous interval exists or they don't overlap, add a new one
        if not merged or merged[-1][1] < current_interval[0]:
            merged.append(current_interval)
        else:
            # Otherwise extend the last interval to cover both
            prev_start, prev_end = merged.pop()
            merged.append((prev_start, max(prev_end, current_interval[1])))
            
    return merged
