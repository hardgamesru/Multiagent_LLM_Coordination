def parse_csv_line(line: str) -> list[str]:
    if not line:
        return []
    result = []
    quote = False
    current_field = ''
    for char in line:
        if char == '"' and not quote:
            quote = True
        elif char == ',' and not quote:
            result.append(current_field.strip())
            current_field = ''
        else:
            current_field += char
            if char == '"' and quote:
                current_field += char
                quote = False
    result.append(current_field.strip())
    return result
