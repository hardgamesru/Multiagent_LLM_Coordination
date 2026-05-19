def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if any(start > end for start, end in intervals):
        raise ValueError("Start cannot be greater than end")
    
    merged = []
    for interval in sorted(intervals, key=lambda x: x[0]):
        if merged and interval[0] <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
        else:
            merged.append(interval)
    return merged
