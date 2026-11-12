def split_fields(text: str) -> list[str]:
    result = []
    quoted = False
    current_field = ''
    
    for char in text:
        if quoted:
            # If quoted, backspace escapes next char and both are discarded
            if char == '\\':
                continue
            elif char == '"':
                quoted = False
            else:
                current_field += char
        else:
            # Not quoted, process normal characters
            if char == ';':
                result.append(current_field.strip())
                current_field = ''
            elif char == '"' or char == "'":
                quoted = True
                current_field += char
            else:
                current_field += char
    
    # Add last field if any
    if current_field:
        result.append(current_field.strip())
    
    return result if result else [""]
