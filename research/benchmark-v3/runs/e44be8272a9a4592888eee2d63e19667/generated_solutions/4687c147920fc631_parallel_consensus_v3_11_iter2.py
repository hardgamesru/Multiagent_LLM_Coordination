def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        result = []
        for interval in intervals:
            if not result or interval[0] > result[-1][1]:
                # No overlap, add new interval
                result.append(interval[:])
            else:
                # Merge with previous interval
                result[-1][1] = max(result[-1][1], interval[1])
        return result

    # Sort both lists of intervals by start value
    base.sort()
    cuts.sort()
    
    # Filter out empty intervals
    base = [(s,e) for s,e in base if s<e]
    cuts = [(s,e) for s,e in cuts if s<e]
    
    # Handle empty cases
    if not base or not cuts:
        return []
    
    # Helper function to check if an interval is fully contained within another
    def contains(a, b):
        return a[0] >= b[0] and a[1] <= b[1]
    
    # Subtract cuts from base
    result = []
    i = j = 0
    while i < len(base):
        current = base[i]
        
        # Find first cut that doesn't contain current interval
        while j < len(cuts) and contains(cuts[j], current):
            j += 1
            
        # Add remaining part before first containing cut
        if j > 0:
            prev_cut = cuts[j-1]
            if current[0] > prev_cut[1]:
                result.append([prev_cut[1], current[0]])
                
        # If no cuts contain current interval, keep entire interval
        elif not cuts:
            result.append(current)
        
        # Move to next uncut interval
        i += 1
    
    # Merge overlapping intervals in result
    return merge_intervals(result)
