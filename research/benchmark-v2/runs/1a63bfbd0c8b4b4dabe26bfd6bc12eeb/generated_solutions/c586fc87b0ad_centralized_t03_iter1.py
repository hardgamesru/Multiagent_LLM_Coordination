def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    prepared = prepare_data(intervals)
    prepared.sort(key=lambda x: x[0])
    
    merged_intervals = []
    current_start, current_end = prepared[0]
    
    for start, end in prepared[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            merged_intervals.append((current_start, current_end))
            current_start, current_end = start, end
    
    merged_intervals.append((current_start, current_end))
    
    return merged_intervals
