def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if any(start > end for start, end in intervals):
        raise ValueError("Start cannot be greater than end")
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = []
    for current in sorted_intervals:
        if not merged or current[0] > merged[-1][1]:
            merged.append(current)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], current[1]))
    return merged
