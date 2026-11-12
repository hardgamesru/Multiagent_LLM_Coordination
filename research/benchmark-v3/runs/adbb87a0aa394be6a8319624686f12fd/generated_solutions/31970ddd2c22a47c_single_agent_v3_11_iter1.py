def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            if not result or interval[0] > result[-1][1]:
                result.append(interval)
            else:
                # Merge overlapping intervals
                result[-1][1] = max(result[-1][1], interval[1])
        return result

    base_intervals = [(interval[0], interval[1]) for interval in base if interval]
    cuts_intervals = [(interval[0], interval[1]) for interval in cuts if interval]
    
    # Sort intervals by start time
    base_intervals.sort()
    cuts_intervals.sort()

    # Subtract cuts from base using two pointers
    merged_base = []
    i = j = 0
    while i < len(base_intervals):
        if j >= len(cuts_intervals):
            # Add remaining base intervals
            merged_base.extend(base_intervals[i:])
            break
        
        if base_intervals[i][0] < cuts_intervals[j][0]:
            # No intersection with current cut
            merged_base.append(base_intervals[i])
            i += 1
        elif base_intervals[i][1] <= cuts_intervals[j][1]:
            # Entirely inside cut interval
            i += 1
        else:
            # Intersecting interval
            if base_intervals[i][0] == cuts_intervals[j][0]:
                # Start point matches, check end points
                if base_intervals[i][1] < cuts_intervals[j][1]:
                    # Cut completely covers base interval
                    i += 1
                else:
                    # Extend cut interval to match base's end
                    cuts_intervals[j][1] = base_intervals[i][1]
                    j += 1
            else:
                # Overlapping but not starting simultaneously
                # Split base interval into two parts
                merged_base.append([base_intervals[i][0], cuts_intervals[j][0]])
                i += 1
                # Update cut interval end point
                cuts_intervals[j][1] = min(cuts_intervals[j][1], base_intervals[i][1])
                j += 1
    
    # Merge adjacent intervals in result
    return merge_intervals(merged_base)
