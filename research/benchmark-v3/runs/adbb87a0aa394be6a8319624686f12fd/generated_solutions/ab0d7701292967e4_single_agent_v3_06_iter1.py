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
            elif char == '"' and text[-1] != '\\':
                quoted = False
                current_field += char
        else:
            # Outside quoted string, process normal characters
            if char == ';' and not current_field:
                # Empty field between semicolons
                result.append('')
            elif char == '"':
                # Start/end of quoted field
                quoted = True
            elif char == '\\':
                # Escaped character
                escaped = True
            else:
                # Regular character
                current_field += char
    
    # Add final field if any
    if current_field:
        result.append(current_field)
    
    return result
