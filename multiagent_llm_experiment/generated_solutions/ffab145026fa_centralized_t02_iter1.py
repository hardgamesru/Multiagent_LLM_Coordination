def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            # Toggle quote state
            in_quotes = not in_quotes
            
            # Handle escaped double quotes within a quoted string
            if in_quotes and i + 1 < len(line) and line[i+1] == '"':
                current_field += '"'
                i += 1
                
        elif char == ',' and not in_quotes:
            # Add field when encountering unquoted comma
            result.append(current_field)
            current_field = ''
            
        else:
            current_field += char
            
        i += 1
        
    # Add last field after processing all characters
    result.append(current_field)
    
    return result
