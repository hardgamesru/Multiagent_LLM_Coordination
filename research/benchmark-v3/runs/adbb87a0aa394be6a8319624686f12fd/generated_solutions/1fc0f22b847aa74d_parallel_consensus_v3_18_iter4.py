def apply_patch_lines(lines, hunks):
    result = []
    pos = 0
    
    for start, old, new in hunks:
        if not (0 <= start <= len(lines)):
            raise ValueError(f"Invalid start position: {start}")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Check exact match of old text
        if old != lines[start:start + len(old)]:
            raise ValueError(f"Old text does not match at line {start}: expected {old}, found {lines[start:start+len(old)]}")
            
        # Insert new content
        result.extend(new)
        
        pos = start + len(old)
    
    # Append remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
