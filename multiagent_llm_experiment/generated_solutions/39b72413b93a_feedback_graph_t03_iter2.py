def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if len(intervals) == 0:
        return []
    
    # Validate intervals and sort them based on their start value
    validated = []
    for i in intervals:
        if i[0] > i[1]:
            raise ValueError("Invalid interval")
        validated.append(i)
    sorted_intervals = sorted(validated, key=lambda x: x[0])
    
    merged = [sorted_intervals[0]]
    for current_interval in sorted_intervals[1:]:
        last_merged = merged[-1]
        
        # Check overlap between previous and current interval
        if current_interval[0] <= last_merged[1]: 
            # Overlap exists; update the end point to max of both ends
            merged[-1] = (last_merged[0], max(last_merged[1], current_interval[1]))
        else:
            # No overlap; add new interval
            merged.append(current_interval)
            
    return merged
