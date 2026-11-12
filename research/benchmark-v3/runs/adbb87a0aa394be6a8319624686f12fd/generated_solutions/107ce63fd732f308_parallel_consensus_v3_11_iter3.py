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
    base_starts = sorted(start for interval in base for start, _ in [interval])
    base_ends = sorted(end for interval in base for _, end in [interval])
    cut_starts = sorted(start for interval in cuts for start, _ in [interval])
    cut_ends = sorted(end for interval in cuts for _, end in [interval])
    
    # Check for reversed intervals
    if any(s > e for s, e in zip(base_starts + cut_starts, base_ends + cut_ends)):
        raise ValueError("Interval is reversed")
    
    # Find gaps after removing cuts from base
    gaps = []
    i = j = k = l = 0
    while i < len(base_starts):
        # Skip empty intervals
        if base_starts[i] == base_ends[i]:
            i += 1
            continue
        
        # Find first cut that overlaps current base interval
        while j < len(cut_starts) and cut_starts[j] < base_ends[i]:
            j += 1
            
        # Add gap between previous cut and current base interval
        if k > 0:
            gaps.append([base_ends[k-1], base_starts[i]])
        
        # Move to next base interval
        k = i
        i += 1
    
    # Add final gap after last base interval
    if k > 0:
        gaps.append([base_ends[k-1], base_ends[-1]])
    
    # Merge adjacent gaps into maximal intervals
    return merge_intervals(gaps)
