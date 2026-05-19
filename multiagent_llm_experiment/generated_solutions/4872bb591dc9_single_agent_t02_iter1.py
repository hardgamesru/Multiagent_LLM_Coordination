def parse_csv_line(line: str) -> list[str]:
    result = []
    quote_mode = False
    current_field = ''
    
    for char in line:
        if char == '"':
            quote_mode = not quote_mode
        elif char == ',' and not quote_mode:
            result.append(current_field.strip())
            current_field = ''
        else:
            current_field += char
    
    result.append(current_field.strip())
    return result
