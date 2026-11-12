def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for start, end in intervals:
            if result and start <= result[-1][1]:
                # Merge overlapping or touching intervals
                result[-1] = [min(result[-1][0], start), max(result[-1][1], end)]
            else:
                result.append([start, end])
        return result
    
    # Combine base and cuts into one set of intervals
    combined = [(s,e) for b in base for s,e in [b]] + [(c[0], c[1]) for c in cuts]
    
    # Sort combined intervals by starting point
    combined.sort()
    
    # Filter out empty intervals and reverse order errors
    valid_intervals = [(s,e) for s,e in combined if s < e and s <= e]
    
    # Subtract cuts from base using difference algorithm
    diff = []
    i = j = 0
    while i < len(valid_intervals):
        while j < len(valid_intervals) and valid_intervals[j][0] < valid_intervals[i][1]:
            # If current cut overlaps with base interval
            if valid_intervals[j][1] >= valid_intervals[i][0]:
                # Adjust start time if needed
                valid_intervals[i][0] = max(valid_intervals[i][0], valid_intervals[j][1])
            j += 1
        # Add remaining part of base interval after cuts
        if valid_intervals[i][1] > valid_intervals[i][0]:
            diff.append(valid_intervals[i])
        i += 1
    
    # Merge adjacent intervals that touch
    return merge_intervals(diff)
