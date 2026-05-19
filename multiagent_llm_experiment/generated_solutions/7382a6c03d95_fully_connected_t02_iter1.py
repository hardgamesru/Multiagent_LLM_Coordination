def parse_csv_line(line: str) -> list[str]:
    result = []
    i = 0
    n = len(line)
    
    while i < n:
        if line[i] == '"':
            # Handle quoted field
            j = i + 1
            value = ''
            while j < n:
                if line[j] == '"':
                    if j+1 < n and line[j+1] == '"': 
                        # Escaped double quote
                        value += '"'
                        j += 2
                    else:
                        break
                else:
                    value += line[j]
                    j += 1
            result.append(value)
            i = j + 2  # Skip closing quote
        else:
            # Handle non-quoted field
            j = i
            while j < n and line[j] != ',':
                j += 1
            result.append(line[i:j])
            i = j + 1
            
    return result
