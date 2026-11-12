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
                # Close quote marks end of quoted field
                if char == '"' or char == "'":
                    quoted = False
                    current_field += char
                else:
                    current_field += char
        else:
            # Outside quoted string, semicolon separates fields
            if char == ';':
                result.append(current_field.strip())
                current_field = ''
            elif char == '"':
                # Start/end of quoted field
                quoted = True
            else:
                # Accumulate characters until separator found
                current_field += char
    
    # Add last field if any
    if current_field:
        result.append(current_field.strip())
    
    return result
