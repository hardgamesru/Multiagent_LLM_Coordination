def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            if not result or interval[0] > result[-1][1]:
                # No overlap, add new interval
                result.append(interval[:])
            else:
                # Overlap, merge with previous interval
                prev_end = result[-1][1]
                result[-1][1] = max(prev_end, interval[1])
        return result

    # Combine base and cuts into one set of intervals
    combined = base + cuts
    
    # Sort intervals by start time
    combined.sort()

    # Remove empty intervals and reverse order of cuts to simulate subtraction
    valid_intervals = [(s, e) for s, e in combined if s < e]
    valid_cuts = [(e, s) for s, e in reversed(combined)]

    # Subtract cuts from base using merge algorithm
    result = merge_intervals(valid_intervals)
    for cut_start, cut_end in valid_cuts:
        # Find overlapping intervals to remove
        i = 0
        while i < len(result):
            if result[i][0] >= cut_start and result[i][1] <= cut_end:
                # Exact match, remove interval
                del result[i]
            elif result[i][0] < cut_start and result[i][1] > cut_end:
                # Interval fully contains cut, split it
                result[i] = [result[i][0], cut_start]
                result.insert(i+1, [cut_end, result[i][1]])
                i += 1
            elif result[i][0] < cut_start and result[i][1] < cut_end:
                # Left part overlaps, adjust current interval
                result[i] = [result[i][0], cut_start]
            elif result[i][0] > cut_start and result[i][1] > cut_end:
                # Right part overlaps, create new interval after current
                result.insert(i+1, [cut_end, result[i][1]])
                i += 1
            i += 1

    # Merge remaining intervals that touch
    return merge_intervals(result)
