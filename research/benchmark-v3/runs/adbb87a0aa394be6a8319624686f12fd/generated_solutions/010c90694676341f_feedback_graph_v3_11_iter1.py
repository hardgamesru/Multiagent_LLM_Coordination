def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            if not result or interval[0] > result[-1][1]:
                # No overlap, add new interval
                result.append(interval)
            else:
                # Merge with previous interval
                prev_end = result[-1][1]
                result[-1][1] = max(prev_end, interval[1])
        return result
    
    # Convert to sorted lists of start/end points
    base_starts = sorted(start for start, _ in base)
    base_ends = sorted(end for _, end in base)
    cut_starts = sorted(start for start, _ in cuts)
    cut_ends = sorted(end for _, end in cuts)
    
    # Find intersections between base and cuts
    i = j = k = l = 0
    overlaps = []
    while i < len(base_starts) and j < len(cut_starts):
        if base_starts[i] == cut_starts[j]:
            # Exact match, skip both
            i += 1
            j += 1
        elif base_starts[i] < cut_starts[j]:
            # Move base forward
            i += 1
        else:
            # Move cut forward
            j += 1
    
    while k < len(base_starts) and l < len(cut_ends):
        if base_starts[k] < cut_ends[l]:
            # Base interval is within a cut interval
            overlaps.append([base_starts[k], min(base_ends[k], cut_ends[l])])
            k += 1
        else:
            # Move cut backward
            l -= 1
            if l < 0:
                break
    
    # Subtract overlapping intervals from base
    remaining_base = []
    for b_start, b_end in base:
        if not overlaps or b_start > overlaps[-1][1]:
            # Interval before first overlap
            remaining_base.append([b_start, b_end])
        else:
            # Remove overlapped parts
            for o_start, o_end in overlaps:
                if b_start >= o_start and b_end <= o_end:
                    # Entirely inside an overlap
                    break
                elif b_start < o_start and b_end <= o_end:
                    # Partially before overlap
                    remaining_base.append([b_start, o_start])
                    break
                elif b_start >= o_start and b_end > o_end:
                    # Partially after overlap
                    remaining_base.append([o_end, b_end])
                    break
                elif b_start < o_start and b_end > o_end:
                    # Split into two parts
                    remaining_base.extend([[b_start, o_start], [o_end, b_end]])
                    break
    
    # Merge remaining intervals
    return merge_intervals(remaining_base)
