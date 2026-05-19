def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    i = 0
    length = len(line)
    
    while i < length:
        char = line[i]
        
        if char == '"':
            # Start of a quoted field
            j = i + 1
            
            while j < length:
                next_char = line[j]
                
                if next_char == '"':
                    # Check for escaped double quote ("")
                    if j+1 < length and line[j+1] == '"':
                        current_field += '"'
                        j += 2
                    else:
                        break
                else:
                    current_field += next_char
                    
                j += 1
            
            i = j + 1
        elif char == ',':
            result.append(current_field.strip() if not current_field.startswith('"') else current_field)
            current_field = ''
            i += 1
        else:
            current_field += char
            i += 1
    
    if current_field:
        result.append(current_field.strip() if not current_field.startswith('"') else current_field)
    
    return result
