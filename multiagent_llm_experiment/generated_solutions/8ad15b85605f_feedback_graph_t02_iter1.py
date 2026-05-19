def parse_csv_line(line: str) -> list[str]:
    if not line.strip():
        return []
    
    result = []
    current_field = ''
    in_quotes = False
    i = 0
    
    while i < len(line):
        char = line[i]
        
        # Handle escaping of double quotes inside quoted fields
        if char == '"' and in_quotes and i + 1 < len(line) and line[i+1] == '"':
            current_field += '"'
            i += 1
            
        elif char == ',' and not in_quotes:
            result.append(current_field)
            current_field = ''
            
        elif char == '"':
            in_quotes = not in_quotes
            
        else:
            current_field += char
            
        i += 1
        
    # Add last field
    result.append(current_field)
    
    # Remove leading/trailing spaces from non-quoted fields
    for j in range(len(result)):
        if not any(c == '"' for c in result[j]):
            result[j] = result[j].strip()
            
    return [field.lstrip('"').rstrip('"') for field in result]
