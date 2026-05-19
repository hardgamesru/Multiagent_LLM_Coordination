def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        # Handle start/end of quoted section
        if char == '"':
            j = i + 1
            while j < len(line) and line[j:j+2] != '""' and line[j] != '"':
                current_field += line[j]
                j += 1
            
            # Add escaped double-quote if found
            if j < len(line) and line[j:j+2] == '""':
                current_field += '"'
                j += 2
                
            # Check for closing quote
            elif j < len(line) and line[j] == '"':
                in_quotes = not in_quotes
                j += 1
            
            i = j - 1  # Move index after processing quoted segment
        else:
            # If outside quotes, split on commas
            if not in_quotes and char == ',':
                result.append(current_field)
                current_field = ''
            else:
                current_field += char
        
        i += 1
    
    # Append last field
    if current_field.strip() or len(result) > 0:
        result.append(current_field)
    
    return result
