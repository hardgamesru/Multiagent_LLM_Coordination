def merge_intervals(intervals):
    if any(start > end for start, end in intervals):
        raise ValueError("Interval start cannot be greater than its end")
    
    sorted_intervals = sorted(intervals)
    merged = []

    for current_start, current_end in sorted_intervals:
        if not merged or merged[-1][1] < current_start - 1:
            merged.append((current_start, current_end))
        else:
            last_start, _ = merged.pop()
            new_interval = (last_start, max(current_end, merged[-1][1]) if merged else current_end)
            merged.append(new_interval)
            
    return merged
