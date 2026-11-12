def parse_csv_line(line: str) -> list[str]:
    result = []
    i, n = 0, len(line)
    while i < n:
        if line[i] == '"':
            # Skip initial quote
            i += 1
            # Find closing quote
            j = line.find('"', i)
            if j == -1:
                raise ValueError(f"Mismatched quotes at position {i}")
            # Add content between quotes, escaping inner quotes
            field = line[i+1:j].replace('""', '"')
            result.append(field)
            i = j + 1
        else:
            # Find next comma or end of string
            j = line.find(',', i)
            if j == -1:
                field = line[i:]
                i = n
            else:
                field = line[i:j]
                i = j + 1
            result.append(field)
    return result
