def parse_csv_line(line: str) -> list[str]:
    fields = []
    field = []
    in_quotes = False
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if in_quotes:
            if c == '"':
                if i + 1 < n and line[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(c)
        else:
            if c == ',':
                fields.append(''.join(field))
                field = []
            elif c == '"':
                in_quotes = True
            else:
                field.append(c)
        i += 1
    fields.append(''.join(field))
    return fields
