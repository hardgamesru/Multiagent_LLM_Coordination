def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    result = []
    quote_mode = False
    current_field = ''
    for char in line:
        if char == ',' and not quote_mode:
            result.append(current_field.strip())
            current_field = ''
        elif char == '"' and not quote_mode:
            quote_mode = not quote_mode
        else:
            current_field += char
    result.append(current_field.strip())
    return [field.strip('"') for field in result]
