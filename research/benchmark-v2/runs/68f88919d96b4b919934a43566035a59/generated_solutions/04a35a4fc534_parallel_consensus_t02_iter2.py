def parse_csv_line(line: str) -> list[str]:
    fields: list[str] = []
    field: list[str] = []
    in_quotes = False
    i = 0
    while i < len(line):
        c = line[i]
        if in_quotes:
            if c == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(c)
        else:
            if c == ',':
                fields.append(''.join(field))
                field.clear()
            elif c == '"':
                in_quotes = True
            else:
                field.append(c)
        i += 1
    fields.append(''.join(field))
    return fields
