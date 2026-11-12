def split_fields(text: str) -> list[str]:
    result = []
    quoted = False
    current_field = ''
    
    for char in text:
        if quoted:
            # Escape sequence: backslash before another character
            if char == '\\':
                current_field += next_char := text[text.index(char)+1]
            else:
                # End of quoted section
                if char == '"' or char == "'":
                    quoted = False
                    current_field += char
                else:
                    current_field += char
        else:
            # Regular character processing
            if char == '"':
                quoted = True
            elif char == ';':
                # Add current field with preserved spaces
                result.append(current_field.strip())
                current_field = ''
            else:
                current_field += char
    
    # Handle last field or unfinished quoted string
    if quoted:
        raise ValueError("Unclosed quote")
    else:
        result.append(current_field.strip())
    
    return result
