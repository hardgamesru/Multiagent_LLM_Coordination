def split_fields(text: str) -> list[str]:
    result = []
    in_quote = False
    current_field = ''
    
    for char in text:
        if in_quote:
            # Inside quoted section, handle escaping and closing quote
            if char == '\\':
                current_field += next_char := text[text.index(char)+1]
            elif char == next_char:
                # Matching closing quote, end of quoted section
                in_quote = False
                current_field += char
            else:
                current_field += char
        else:
            # Outside quoted section, handle normal characters and semicolon separation
            if char == '"':
                in_quote = True
                continue
            elif char == ';':
                result.append(current_field.strip())
                current_field = ''
            else:
                current_field += char
    
    # Add last field if any
    if current_field:
        result.append(current_field.strip())
    
    return result if result else [""]
