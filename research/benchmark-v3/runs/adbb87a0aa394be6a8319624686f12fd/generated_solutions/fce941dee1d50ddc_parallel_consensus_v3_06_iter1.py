def split_fields(text: str) -> list[str]:
    result = []
    quoted = False
    current_field = ''
    
    for char in text:
        if quoted:
            # Escape sequence processing
            if char == '\\':
                continue
            elif char == '"' and text[-2] != '\\':
                quoted = False
                # Remove opening quote from current field
                current_field = current_field[1:]
            else:
                current_field += char
        else:
            # Regular character processing
            if char == '"':
                quoted = True
                # Add closing quote to current field
                current_field += '"'
            elif char == ';':
                # Add processed field to result
                result.append(current_field.strip())
                current_field = ''
            else:
                current_field += char
    
    # Handle last field or unmatched quote
    if quoted:
        raise ValueError("Unclosed quote")
    else:
        result.append(current_field.strip())
    
    return result
