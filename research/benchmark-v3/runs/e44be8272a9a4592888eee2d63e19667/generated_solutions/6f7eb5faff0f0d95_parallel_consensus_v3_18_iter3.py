def apply_patch_lines(lines, hunks):
    if not hunks or not lines:
        return lines[:]
    
    result = []
    pos = 0
    
    for start, old, new in hunks:
        if start < 0 or len(lines) < start + len(old):
            raise ValueError("Invalid patch range")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Check exact match of old text
        if lines[start:start+len(old)] != old:
            raise ValueError("Patch does not match")
            
        # Insert new content from hunk
        result.extend(new)
        
        # Update position after processed hunk
        pos = start + len(old)
    
    # Append remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
