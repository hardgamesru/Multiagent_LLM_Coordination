def parse_csv_line(line: str) -> list[str]:
    result = []
    i, n = 0, len(line)
    
    while i < n:
        if line[i] == '"':
            j = i + 1
            value = ''
            while j < n:
                if line[j] == '"' and (j+1 >= n or line[j+1] != '"'):
                    break
                elif line[j:j+2] == '""':
                    value += '"'
                    j += 2
                else:
                    value += line[j]
                    j += 1
            result.append(value)
            i = j + 2
        else:
            j = i
            while j < n and line[j] != ',':
                j += 1
            result.append(line[i:j])
            i = j + 1
            
    return [val.strip() for val in result]
