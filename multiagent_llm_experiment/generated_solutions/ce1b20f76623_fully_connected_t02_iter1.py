def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    in_quotes = False
    i = 0
    
    while i < len(line):
        char = line[i]
        
        if char == '"':
            # Check for escaped double quote
            if in_quotes and i + 1 < len(line) and line[i+1] == '"':
                current_field += '"'
                i += 1  # Skip next double quote
            else:
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            result.append(current_field)
            current_field = ''
        else:
            current_field += char
            
        i += 1
    
    result.append(current_field)
    return result
