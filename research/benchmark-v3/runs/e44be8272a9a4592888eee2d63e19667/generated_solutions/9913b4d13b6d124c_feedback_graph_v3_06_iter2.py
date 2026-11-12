def split_fields(text: str) -> list[str]:
    result = []
    quoted = False
    current_field = ''
    
    for char in text:
        if quoted:
            # Inside quoted string, backslash escapes next character
            if char == '\\':
                current_field += char + next_char := next(text)
            else:
                # Close quote or normal character
                if char == '"' or char == "'":
                    quoted = False
                    current_field += char
                else:
                    current_field += char
        else:
            # Outside quoted string, handle semicolon and backslash
            if char == ';':
                result.append(current_field.strip())
                current_field = ''
            elif char == '"':
                quoted = True
                current_field += char
            elif char == '\\':
                # Escaped character
                try:
                    next_char := next(text)
                    current_field += next_char
                except StopIteration:
                    raise ValueError("Dangling escape")
            else:
                current_field += char
    
    # Add last field if any
    if current_field:
        result.append(current_field.strip())
    
    return result
