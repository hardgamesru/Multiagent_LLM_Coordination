def split_fields(text: str) -> list[str]:
    result = []
    quoted = False
    escaped = False
    current_field = ''
    
    for char in text:
        if escaped:
            # Escape sequence processed, remove backslash
            current_field += char
            escaped = False
        elif quoted:
            # Inside quoted string, handle escaping and closing quote
            if char == '\\':
                escaped = True
            elif char == '"' and (len(current_field) == 0 or current_field[-1] != '"'):
                # Close quote, add field to result
                result.append(current_field)
                current_field = ''
                quoted = False
            else:
                current_field += char
        else:
            # Outside quotes, process normal characters
            if char == ';' and len(current_field):
                # Separate fields unless last character was escaped
                result.append(current_field)
                current_field = ''
            elif char in ('"', "'"):
                # Start/end of quoted field
                quoted = True
                current_field += char
            else:
                current_field += char
                
    # Add remaining field if any
    if len(current_field):
        result.append(current_field)
        
    return result
