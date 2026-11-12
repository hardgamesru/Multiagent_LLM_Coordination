def apply_patch_lines(lines, hunks):
    if not hunks or not lines:
        return lines[:]
    
    result = []
    pos = 0
    
    for start, old, new in hunks:
        if start < 0 or start > len(lines):
            raise ValueError("Invalid start index")
        
        # Check that old matches exactly
        if lines[pos:pos + len(old)] != old:
            raise ValueError("Old content mismatch")
            
        # Add unchanged part before current hunk
        result.extend(lines[pos:start])
        
        # Insert new content from hunk
        result.extend(new)
        
        # Update position after processed range
        pos = start + len(old)
    
    # Append remaining unmodified lines
    result.extend(lines[pos:])
    
    return result
