def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if any(start > end for start, end in intervals):
        raise ValueError("Start cannot be greater than end")
    sorted_intervals = sorted(intervals)
    result = []
    current_start, current_end = sorted_intervals[0]
    for start, end in sorted_intervals[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            result.append((current_start, current_end))
            current_start, current_end = start, end
    result.append((current_start, current_end))
    return result
