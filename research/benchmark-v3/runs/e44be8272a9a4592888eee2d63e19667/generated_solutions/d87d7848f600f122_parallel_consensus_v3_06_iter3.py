def split_fields(text: str) -> list[str]:
    if not text:
        return [""]
    
    result = []
    quoted = False
    escaped = False
    current_field = ""
    
    for char in text:
        if escaped:
            # Remove backslash and add next character to current field
            current_field += char
            escaped = False
        elif quoted:
            # If quoted, treat closing quote as normal character
            if char == quoted:
                quoted = False
                current_field += char
            else:
                current_field += char
        elif char == '"':
            # Start/end of quoted field
            quoted = '"'
        elif char == "'":
            # Start/end of quoted field
            quoted = "'"
        elif char == ';':
            # Regular separator
            if current_field:
                result.append(current_field.strip())
                current_field = ""
        else:
            # Accumulate non-quoted characters
            current_field += char
            
    # Add last field if any
    if current_field:
        result.append(current_field.strip())
        
    return result
