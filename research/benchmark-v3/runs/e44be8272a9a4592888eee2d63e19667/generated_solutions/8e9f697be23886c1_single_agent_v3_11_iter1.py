def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            if not result or interval[0] > result[-1][1]:
                # No overlap, add new interval
                result.append(interval)
            else:
                # Merge with last interval
                result[-1][1] = max(result[-1][1], interval[1])
        return result

    base_intervals = [(interval[0], interval[1]) for interval in base if interval[0] < interval[1]]
    cuts_intervals = [(interval[0], interval[1]) for interval in cuts if interval[0] < interval[1]]
    
    if any(i[0] >= i[1] for i in cuts_intervals + base_intervals):
        raise ValueError("Invalid interval")
    
    # Sort intervals by start point
    base_intervals.sort()
    cuts_intervals.sort()
    
    # Subtract cuts from base
    merged_base = []
    i = j = 0
    while i < len(base_intervals) and j < len(cuts_intervals):
        if base_intervals[i][0] < cuts_intervals[j][0]:
            # Base interval starts before cut, check for intersection
            if base_intervals[i][1] <= cuts_intervals[j][0]:
                # No intersection, move to next base interval
                i += 1
            elif base_intervals[i][1] < cuts_intervals[j][1]:
                # Full intersection, skip both
                i += 1
                j += 1
            else:
                # Partial intersection, split base interval
                merged_base.append([base_intervals[i][0], cuts_intervals[j][0]])
                i += 1
                j += 1
        else:
            # Cut starts earlier, check for full containment
            if cuts_intervals[j][1] <= base_intervals[i][0]:
                # No intersection, move to next cut
                j += 1
            elif cuts_intervals[j][1] < base_intervals[i][1]:
                # Full containment, remove entire base interval
                i += 1
            else:
                # Partial containment, split cut interval
                merged_base.append([cuts_intervals[j][0], base_intervals[i][0]])
                j += 1
    
    # Add remaining base intervals
    while i < len(base_intervals):
        merged_base.append(base_intervals[i])
        i += 1
    
    # Merge overlapping intervals in result
    return merge_intervals(merged_base)
