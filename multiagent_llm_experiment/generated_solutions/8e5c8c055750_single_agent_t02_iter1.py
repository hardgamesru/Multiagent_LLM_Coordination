def parse_csv_line(line: str) -> list[str]:
    result = []
    quote_mode = False
    current_field = ''
    
    for char in line:
        if char == '"' and not quote_mode:
            quote_mode = True
        elif char == '"' and quote_mode:
            current_field += char
            quote_mode = False
        elif char == ',' and not quote_mode:
            result.append(current_field.strip())
            current_field = ''
        else:
            current_field += char
    
    result.append(current_field.strip())
    return result
