def split_fields(text: str) -> list[str]:
    result = []
    quoted = False
    escaped = False
    current_field = ''
    
    for char in text:
        if escaped:
            # Escape sequence processed, reset flag
            current_field += char
            escaped = False
        elif quoted:
            # Inside quoted string, handle closing quote and content
            if char == '"' and not escaped:
                quoted = False
                result.append(current_field)
                current_field = ''
            else:
                current_field += char
        elif char == '"':
            # Start of quoted string
            quoted = True
        elif char == ';':
            # Regular separator, add current field if non-empty
            if current_field:
                result.append(current_field)
                current_field = ''
        else:
            # Normal character, accumulate into current field
            current_field += char
            if char == '\\':
                # Escaped character detected
                escaped = True
    
    # Add last field if non-empty after processing
    if current_field:
        result.append(current_field)
    
    return result
