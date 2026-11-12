def parse_csv_line(line: str) -> list[str]:
    result, chars, i = [], [], 0
    while i < len(line):
        if line[i] == '"':
            i += 1
            while i < len(line) and line[i] != '"':
                if line[i] == ',':
                    chars.append(line[i])
                else:
                    chars.append(line[i])
                i += 1
            i += 1
        else:
            while i < len(line) and line[i] != ',':
                chars.append(line[i])
                i += 1
            result.append(''.join(chars).rstrip(',').strip('"'))
            chars.clear()
    return result
