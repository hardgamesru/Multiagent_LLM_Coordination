def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        # Handle start or end of quoted section
        if char == '"':
            j = i + 1
            
            # Find next closing quote
            while j < len(line) and line[j] != '"' or (j > i+1 and line[j-1] == '"'):
                j += 1
                
            # Extract content between quotes
            inner_content = line[i+1:j]
            
            # Replace double-quote escape sequences
            current_field += inner_content.replace('""', '"')
            
            # Move past closing quote
            i = j + 1
            
            # Check for trailing comma after quote
            if i < len(line) and line[i] == ',':
                result.append(current_field)
                current_field = ''
                i += 1
            else:
                in_quotes = False
                
        elif char == ',':
            # If outside quotes, split here
            if not in_quotes:
                result.append(current_field)
                current_field = ''
            i += 1
        else:
            # Regular character, add to current field
            current_field += char
            i += 1
            
    # Add last field if any
    if current_field:
        result.append(current_field)
        
    return result
