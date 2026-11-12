def split_fields(text: str) -> list[str]:
    result = []
    quoted = False
    escaped = False
    current_field = ''
    
    for char in text:
        if escaped:
            # Escape sequence: remove backslash and add next character
            current_field += char
            escaped = False
        elif char == '\\':
            # Start of escape sequence
            escaped = True
        elif quoted:
            # Inside quoted string
            if char == '"' and text[text.index(char)-1] != '\\':
                # Matching closing quote
                quoted = False
            else:
                # Keep characters inside quotes
                current_field += char
        elif char == '"':
            # Start/end of quoted field
            quoted = True
        elif char == ';':
            # Field separator outside quotes
            if current_field:
                result.append(current_field)
                current_field = ''
        else:
            # Accumulate non-separator characters
            current_field += char
    
    # Add last field if any
    if current_field:
        result.append(current_field)
    
    return result
