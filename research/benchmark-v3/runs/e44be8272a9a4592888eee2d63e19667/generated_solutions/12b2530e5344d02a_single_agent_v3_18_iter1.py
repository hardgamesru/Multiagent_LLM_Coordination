def apply_patch_lines(lines: list[str], hunks: list[list]):
    result = []
    pos = 0
    
    for start, old, new in hunks:
        if not (0 <= start < len(lines)):
            raise ValueError("Invalid start position")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Check exact match of old lines
        if old != lines[start:start + len(old)]:
            raise ValueError(f"Old line mismatch at position {start}")
            
        # Insert new content
        result.extend(new)
        
        pos = start + len(old)
    
    # Append remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
