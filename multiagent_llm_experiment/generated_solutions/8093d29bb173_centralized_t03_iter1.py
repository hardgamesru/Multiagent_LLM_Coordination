def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    for i in intervals:
        if len(i) != 2 or i[0] > i[1]:
            raise ValueError("Invalid interval")
    
    sorted_intervals = sorted(intervals)
    
    merged = []
    for current_interval in sorted_intervals:
        if not merged or merged[-1][1] < current_interval[0]:
            merged.append(current_interval)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], current_interval[1]))
    
    return merged
