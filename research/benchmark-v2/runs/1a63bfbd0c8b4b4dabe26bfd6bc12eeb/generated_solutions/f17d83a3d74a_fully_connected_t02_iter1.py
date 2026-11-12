def parse_csv_line(line: str) -> list[str]:
    result, current_field, quote_mode = [], '', False
    for char in line:
        if char == '"' and not quote_mode:
            quote_mode = not quote_mode
        elif char == ',' and not quote_mode:
            result.append(current_field.strip())
            current_field = ''
        else:
            if char == '"' and quote_mode:
                current_field += '"'
            current_field += char
    result.append(current_field.strip())
    return result
