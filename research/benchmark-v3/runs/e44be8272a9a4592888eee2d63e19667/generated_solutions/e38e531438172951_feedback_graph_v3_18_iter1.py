def apply_patch_lines(lines, hunks):
    if not hunks or not lines:
        return lines[:]
    
    result = []
    pos = 0
    for start, old, new in hunks:
        if start < 0 or start > len(lines):
            raise ValueError("Invalid start position")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Check exact length match between old values and existing text
        if len(old) != sum(1 for l in lines[start:start+len(old)] if l in old):
            raise ValueError("Old value does not match exactly")
            
        # Replace matching section with new content
        result.extend(new)
        
        # Update position after processed hunk
        pos = start + len(old)
    
    # Append remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
