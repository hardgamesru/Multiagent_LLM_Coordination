def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # Validate input
    for i in intervals:
        if len(i) != 2 or i[0] > i[1]:
            raise ValueError("Invalid interval")
    
    # Sort intervals based on their start point
    sorted_intervals = sorted(intervals)
    
    merged = []
    for current_interval in sorted_intervals:
        # If no previous interval or non-overlapping with last one
        if not merged or merged[-1][1] < current_interval[0]:
            merged.append(current_interval)
        else:
            # Overlap exists; update the end of the last interval
            merged[-1] = (merged[-1][0], max(merged[-1][1], current_interval[1]))
    
    return merged
