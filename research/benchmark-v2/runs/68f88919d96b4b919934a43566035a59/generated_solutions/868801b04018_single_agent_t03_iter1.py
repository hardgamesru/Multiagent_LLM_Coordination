def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    for s, e in intervals:
        if s > e:
            raise ValueError("Interval start cannot be greater than end.")
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    for current in sorted_intervals[1:]:
        last_s, last_e = merged[-1]
        curr_s, curr_e = current
        if curr_s <= last_e:
            merged[-1] = (last_s, max(last_e, curr_e))
        else:
            merged.append(current)
    return merged
