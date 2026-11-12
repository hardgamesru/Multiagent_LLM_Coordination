def parse_csv_line(line: str) -> list[str]:
    fields = []
    field = []
    in_quotes = False
    i = 0
    length = len(line)
    while i < length:
        char = line[i]
        if in_quotes:
            if char == '"':
                if i + 1 < length and line[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(char)
        else:
            if char == ',':
                fields.append(''.join(field))
                field = []
            elif char == '"':
                in_quotes = True
            else:
                field.append(char)
        i += 1
    if in_quotes:
        raise ValueError("Unmatched quote in CSV line")
    fields.append(''.join(field))
    return fields
