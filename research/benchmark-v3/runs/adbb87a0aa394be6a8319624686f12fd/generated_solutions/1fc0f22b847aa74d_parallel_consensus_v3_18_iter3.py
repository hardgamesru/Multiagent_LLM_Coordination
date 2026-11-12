def apply_patch_lines(lines, hunks):
    result = []
    pos = 0
    
    for start, old, new in hunks:
        if start < 0 or start > len(lines):
            raise ValueError("Invalid start position")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Check exact match of old text
        if old != lines[start:start + len(old)]:
            raise ValueError("Old text does not match")
            
        # Insert new content
        result.extend(new)
        
        pos = start + len(old)
    
    # Append remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
