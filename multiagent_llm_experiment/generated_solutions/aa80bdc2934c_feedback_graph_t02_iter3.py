def parse_csv_line(line: str) -> list[str]:
    result = []
    i = 0
    length = len(line)
    while i < length:
        if line[i] == '"':
            # Skip opening quote
            i += 1
            # Build quoted field
            field = ''
            while i < length and line[i] != '"':
                if line[i:i+2] == '""':
                    field += '"'
                    i += 2
                else:
                    field += line[i]
                    i += 1
            # Skip closing quote
            i += 1
            result.append(field)
        elif line[i] == ',':
            # Skip comma
            i += 1
        else:
            # Build unquoted field
            field = ''
            while i < length and line[i] != ',':
                field += line[i]
                i += 1
            result.append(field)
    return result
