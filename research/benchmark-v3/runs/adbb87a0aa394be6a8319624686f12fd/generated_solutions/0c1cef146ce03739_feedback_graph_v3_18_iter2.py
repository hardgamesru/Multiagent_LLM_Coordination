def apply_patch_lines(lines, hunks):
    if not hunks or not lines:
        return list(lines)
    
    result = []
    pos = 0
    
    for start, old, new in hunks:
        # Check index validity
        if start < 0 or len(lines) < start + len(old):
            raise ValueError(f"Invalid start index: {start}")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Validate exact match of old content
        if lines[start:start+len(old)] != old:
            raise ValueError("Old content does not match")
            
        # Insert new content
        result.extend(new)
        
        # Update position after processing hunk
        pos = start + len(old)
    
    # Append remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
