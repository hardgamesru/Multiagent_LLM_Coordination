def parse_csv_line(line: str) -> list[str]:
    result = []
    field = []
    in_quotes = False
    index = 0
    while index < len(line):
        char = line[index]
        if char == '"':
            if in_quotes and index + 1 < len(line) and line[index + 1] == '"':
                field.append('"')
                index += 1
            else:
                in_quotes = not in_quotes
        elif char == "," and not in_quotes:
            result.append("".join(field))
            field = []
        else:
            field.append(char)
        index += 1
    result.append("".join(field))
    return result
