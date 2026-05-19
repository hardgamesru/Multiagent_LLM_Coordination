def parse_csv_line(line: str) -> list[str]:
    result, in_quote = [], False
    curr_field = ''
    for ch in line:
        if ch == '"':
            in_quote = not in_quote
        elif ch == ',' and not in_quote:
            result.append(curr_field.strip('"'))
            curr_field = ''
        else:
            curr_field += ch
    result.append(curr_field.strip('"'))
    return result
