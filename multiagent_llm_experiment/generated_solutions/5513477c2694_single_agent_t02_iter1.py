def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    in_quotes = False
    
    for char in line:
        if char == '"':
            # Toggle state when we encounter a double-quote
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            # Add current field to results and reset it when encountering unquoted commas
            result.append(current_field)
            current_field = ''
        else:
            # Regular character or comma within quotes, add to current field
            current_field += char
            
    # Add last field after processing all characters
    result.append(current_field.strip('"'))
    
    return [field.replace('""', '"') for field in result]
