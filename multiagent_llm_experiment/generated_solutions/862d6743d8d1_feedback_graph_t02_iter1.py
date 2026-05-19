def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    in_quotes = False
    
    for char in line:
        if char == '"':
            # If we're already in quotes, check for escaping
            if in_quotes and len(current_field) > 0 and current_field[-1] == '"':
                current_field = current_field[:-1] + '"'  
            else:
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            result.append(current_field)
            current_field = ''
        else:
            current_field += char
            
    result.append(current_field)
    return [field.strip('"') for field in result]
