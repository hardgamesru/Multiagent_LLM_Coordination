def apply_patch_lines(lines: list[str], hunks: list[list]):
    result = []
    pos = 0
    
    for start, old, new in hunks:
        if not (0 <= start < len(lines)):
            raise ValueError("Invalid start position")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Check exact match of old lines
        if lines[start:start + len(old)] != old:
            raise ValueError(f"Old lines mismatch at position {start}")
            
        # Insert replacement lines
        result.extend(new)
        
        # Update position after processed hunk
        pos = start + len(old)
    
    # Append remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
