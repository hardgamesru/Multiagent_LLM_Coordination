def apply_patch_lines(lines, hunks):
    if not hunks or not lines:
        return lines[:]
    
    result = []
    pos = 0
    
    for start, old, new in hunks:
        # Check start coordinate is within valid range
        if start < 0 or start > len(lines):
            raise ValueError(f"Invalid start position: {start}")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Validate length of replacement
        if len(old) != (start + len(old) - len(result)):
            raise ValueError("Replacement length mismatch")
        
        # Apply patch: remove old lines and insert new ones
        result.extend(new)
        
        # Update position after processing current hunk
        pos = start + len(old)
    
    # Add remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
