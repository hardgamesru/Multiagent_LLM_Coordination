def subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]:
    def merge_intervals(intervals):
        if not intervals:
            return []
        
        # Sort intervals by start value
        intervals.sort()
        result = []
        current_start = current_end = intervals[0][0]
        
        for start, end in intervals:
            if start > current_end:
                # Add previous interval if it's valid
                result.append([current_start, current_end])
            
            # Update current interval boundaries
            current_start = min(current_start, start)
            current_end = max(current_end, end)
        
        # Add last interval after processing all
        result.append([current_start, current_end])
    
        # Remove zero-length intervals
        return [interval for interval in result if interval[0] != interval[1]]
    
    # Validate input intervals are properly formed
    for interval in base + cuts:
        if len(interval) != 2 or interval[0] >= interval[1]:
            raise ValueError("Invalid interval")
    
    # Convert intervals to sorted list of starts and ends
    starts = sorted(start for interval in base for start, _ in interval)
    ends = sorted(end for _, end in base)
    
    # Subtract cuts from base using two pointers technique
    merged_base = []
    i = j = 0
    while i < len(starts) and j < len(ends):
        if starts[i] < ends[j]:
            # Base interval is active, add its start point
            merged_base.append(starts[i])
            i += 1
        else:
            # Cuts interval covers base, skip it
            j += 1
    
    # If remaining base intervals remain unprocessed
    if i < len(starts):
        merged_base.extend(starts[i:])
    
    # Merge resulting points into intervals
    return merge_intervals(zip(merged_base, merged_base[1:] + [float('inf')]))
