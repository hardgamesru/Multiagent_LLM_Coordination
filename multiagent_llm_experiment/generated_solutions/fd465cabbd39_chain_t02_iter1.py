def parse_csv_line(line: str) -> list[str]:
    if not isinstance(line, str):
        raise TypeError('Input must be a string')
    
    result = []
    current_field = ''
    in_quotes = False
    i = 0
    
    while i < len(line):
        char = line[i]
        
        # Handle end of quoted field
        if char == '"' and in_quotes:
            # Check for doubled quotes
            if i + 1 < len(line) and line[i+1] == '"':
                current_field += '"'
                i += 1
            else:
                in_quotes = False
        elif char == ',' and not in_quotes:
            result.append(current_field.strip('"'))
            current_field = ''
        elif char == '"':
            in_quotes = True
        else:
            current_field += char
            
        i += 1
    
    # Add last field
    result.append(current_field.strip('"'))
    
    # Validate that all quotes were closed properly
    if in_quotes:
        raise ValueError('Unclosed quotation mark found')
    
    return result
