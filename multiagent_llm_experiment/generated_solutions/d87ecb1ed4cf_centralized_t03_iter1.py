def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # Check each interval is valid
    for start, end in intervals:
        if start > end:
            raise ValueError(f"Interval {start}, {end} has invalid order.")
            
    # Sort intervals by starting point
    sorted_intervals = sorted(intervals)
    
    merged = []
    for current_start, current_end in sorted_intervals:
        # If first interval or does not overlap with previous
        if not merged or merged[-1][1] < current_start:
            merged.append((current_start, current_end))
        else:
            # Update last interval's end if needed
            prev_start, prev_end = merged.pop()
            new_end = max(prev_end, current_end)
            merged.append((prev_start, new_end))
            
    return merged
