def apply_patch_lines(lines, hunks):
    if not hunks or not lines:
        return lines[:]
    
    result = []
    pos = 0
    
    for start, old, new in hunks:
        # Check index boundaries and non-overlapping conditions
        if start < 0 or start >= len(lines) or \
           len(old) != sum(len(l) for l in lines[start:start + len(old)]) or \
           any(start + i < pos for i in range(len(old))):
            raise ValueError("Invalid patch")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Replace exact matching section with new content
        result.extend(new)
        
        # Update position after processing current hunk
        pos = start + len(old)
    
    # Append remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
