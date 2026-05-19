def merge_intervals(intervals):
    # Check for invalid intervals
    for start, end in intervals:
        if start > end:
            raise ValueError("Invalid interval")

    # Handle empty input case
    if len(intervals) == 0:
        return []

    # Sort intervals based on start time
    intervals.sort(key=lambda x: x[0])

    # Initialize result array with first interval
    result = [intervals[0]]

    # Iterate through remaining intervals to check overlaps/adjacencies
    for current_start, current_end in intervals[1:]:
        last_merged_interval = result[-1]

        # If there is overlap or adjacency between current and previous interval
        if current_start <= last_merged_interval[1]:
            # Extend the last interval's end if necessary
            result[-1] = (last_merged_interval[0], max(last_merged_interval[1], current_end))
        else:
            # Add non-overlapping interval
            result.append((current_start, current_end))

    return result
