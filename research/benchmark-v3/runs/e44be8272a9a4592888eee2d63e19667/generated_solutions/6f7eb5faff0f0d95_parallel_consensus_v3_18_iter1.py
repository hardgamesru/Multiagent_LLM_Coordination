def apply_patch_lines(lines, hunks):
    if not hunks or not lines:
        return lines[:]
    
    result = []
    pos = 0
    
    for start, old_text, new_text in hunks:
        if start < 0 or start > len(lines):
            raise ValueError("Invalid start position")
        
        # Add unmodified part before current hunk
        result.extend(lines[pos:start])
        
        # Check for empty old text which allows insertion
        if old_text == []:
            result.extend(new_text)
        else:
            # Verify exact match of old text
            if lines[start:start + len(old_text)] != old_text:
                raise ValueError("Old text does not match")
            
            # Replace matched range with new text
            result.extend(new_text)
        
        # Update position after processing current hunk
        pos = start + len(old_text)
    
    # Append remaining unchanged lines
    result.extend(lines[pos:])
    
    return result
