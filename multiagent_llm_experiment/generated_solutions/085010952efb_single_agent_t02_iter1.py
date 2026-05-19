def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    in_quotes = False
    
    for char in line:
        if char == '"':
            # Toggle quoting state, handle escape "" as "
            if in_quotes and len(current_field) > 0 and current_field[-1] == '"':
                current_field = current_field[:-1] + '"'
            else:
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            result.append(current_field)
            current_field = ''
        else:
            current_field += char
            
    # Add last field after loop ends
    result.append(current_field)
    
    return result
