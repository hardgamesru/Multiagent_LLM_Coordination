def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        # Handle escape sequence (doubled double-quote)
        if char == '"' and in_quotes and (i + 1 < len(line)) and line[i+1] == '"':
            current_field += '"'
            i += 1  # Skip next character which is part of escape sequence
            
        elif char == ',' and not in_quotes:
            result.append(current_field.strip('"'))
            current_field = ''  # Reset current field buffer
            
        elif char == '"':  
            in_quotes = not in_quotes  # Toggle state when encountering a quote
            
        else:
            current_field += char
            
        i += 1
        
    # Add last field after processing all characters
    result.append(current_field.strip('"'))
    
    return result
