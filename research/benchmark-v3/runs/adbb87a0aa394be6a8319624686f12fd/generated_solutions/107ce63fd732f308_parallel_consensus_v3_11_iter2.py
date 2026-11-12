def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            if not result or interval[0] > result[-1][1]:
                # No overlap, add new interval
                result.append(interval[:])
            else:
                # Merge with last interval
                result[-1][1] = max(result[-1][1], interval[1])
        return result
    
    # Convert to sorted lists of start/end points
    starts_base = [(s, 'b') for s,e in base for s in [s]]
    ends_base = [(e, 'e') for s,e in base for e in [e]]
    starts_cuts = [(s, 'c') for s,e in cuts for s in [s]]
    ends_cuts = [(e, 'e') for s,e in cuts for e in [e]]
    
    # Sort combined events
    events = sorted(starts_base + starts_cuts + ends_base + ends_cuts)
    
    count = {}
    current_intervals = []
    
    # Process event stream
    for point, typ in events:
        if typ == 'b':
            # Start of an interval
            count[point] = count.get(point, 0) + 1
            if count[point] == 1:
                current_intervals.append([point])
        elif typ == 'c':
            # Cut interval
            count[point] -= 1
            if count[point] == 0:
                # Remove cut interval from active set
                current_intervals.remove([point])
        else:
            # End of interval
            count[point] -= 1
            if count[point] == 0:
                # Add completed interval to result
                current_intervals.pop()
                if current_intervals:
                    # Merge adjacent intervals if needed
                    current_intervals = merge_intervals(current_intervals)
    
    # Convert back to [start, end) format
    result = []
    for interval in current_intervals:
        result.append([interval[0], interval[-1]])
    
    return result
