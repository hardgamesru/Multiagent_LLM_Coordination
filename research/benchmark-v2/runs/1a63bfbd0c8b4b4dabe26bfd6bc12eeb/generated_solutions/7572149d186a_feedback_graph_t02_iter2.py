def parse_csv_line(line: str) -> list[str]:
    result = []
    i, n = 0, len(line)
    while i < n:
        if line[i] == '"':
            # Skip opening quote
            i += 1
            # Read quoted field
            j = i
            while i < n and line[i] != '"':
                if line[i:i+2] == '""':
                    i += 2
                else:
                    i += 1
            # Add field without quotes
            result.append(line[j:i].replace('""', '"'))
            i += 1  # Skip closing quote
        elif line[i] == ',':
            # Add empty field
            result.append('')
            i += 1
        else:
            # Read unquoted field
            j = i
            while i < n and line[i] != ',':
                i += 1
            result.append(line[j:i])
    return result
