def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    for s, e in intervals:
        if s > e:
            raise ValueError("Interval start must not be greater than end")
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    for current in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        cur_start, cur_end = current
        if cur_start <= last_end:
            merged[-1] = (last_start, max(last_end, cur_end))
        else:
            merged.append(current)
    return merged
