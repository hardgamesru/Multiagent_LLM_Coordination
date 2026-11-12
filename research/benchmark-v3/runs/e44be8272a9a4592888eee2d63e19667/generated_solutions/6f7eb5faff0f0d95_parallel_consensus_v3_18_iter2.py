def apply_patch_lines(lines, hunks):
    result = lines[:]
    
    for start, old, new in hunks:
        if start < 0 or len(result) < start or \
           len(old) != (start + len(old)) - start:
            raise ValueError("Invalid patch range")
        
        # Remove old section
        del result[start:start+len(old)]
        
        # Insert new section
        result[start:start] = new
    
    return result
