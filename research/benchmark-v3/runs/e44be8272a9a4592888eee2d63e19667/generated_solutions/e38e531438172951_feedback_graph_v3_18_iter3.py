def apply_patch_lines(lines, hunks):
    if not hunks or not lines:
        return lines[:]
    
    result = lines[:]
    indices = sorted(hunk[0] for hunk in hunks)
    
    # Process each hunk
    for idx, (start, old, new) in zip(indices, hunks):
        # Validate start index is within range
        if start < 0 or start > len(result):
            raise ValueError(f"Invalid start index {start}")
        
        # Validate length of old matches actual slice
        old_len = len(old)
        slice_len = len(result[start:start + old_len])
        if slice_len != old_len:
            raise ValueError("Old value does not match exact slice")
            
        # Replace slice with new values
        result[start:start + old_len] = new
    
    return result
