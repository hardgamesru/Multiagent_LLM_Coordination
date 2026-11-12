def split_fields(text: str) -> list[str]:
    result = []
    quoted = False
    current_field = ''
    
    for char in text:
        if quoted:
            # Inside quoted string, backslash escapes next character
            if char == '\\':
                current_field += next_char := text[text.index(char)+1]  
                continue
            elif char == ('"' if quoted else "'"):
                quoted = False
                # Remove enclosing quote from field
                current_field = current_field[1:-1]
            else:
                # Regular character inside quoted string
                current_field += char
        else:
            # Outside quoted string
            if char == ';':
                # Field separator outside quotes
                result.append(current_field.strip())
                current_field = ''
            elif char in '"\'':
                # Start of quoted string
                quoted = True
                current_field += char
            elif char == '\\':
                # Escaped character
                current_field += next_char := text[text.index(char)+1]
                continue
            else:
                # Regular character outside quotes
                current_field += char
    
    # Add last field if any
    if current_field:
        result.append(current_field.strip())
    
    return result if result else [""]
