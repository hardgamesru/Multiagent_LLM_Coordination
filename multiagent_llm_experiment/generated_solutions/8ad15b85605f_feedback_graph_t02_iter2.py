def parse_csv_line(line: str) -> list[str]:
    if len(line.strip()) == 0:
        return []
    
    parts = []
    current_field = ''
    in_quotes = False
    i = 0
    
    while i < len(line):
        char = line[i]
        
        if char == '"':
            # Toggle state when entering/exiting quotes
            if in_quotes:
                # Check for escaping ("")
                if i + 1 < len(line) and line[i+1] == '"':
                    current_field += '"'
                    i += 1
                else:
                    in_quotes = False
            else:
                in_quotes = True
        elif char == ',' and not in_quotes:
            parts.append(current_field)
            current_field = ''
        else:
            current_field += char
            
        i += 1
    
    # Add last field after processing all chars
    parts.append(current_field)
    
    # Remove leading and trailing spaces outside of quotes
    final_fields = [field.strip() if not any((ch == '"' for ch in field)) else field for field in parts]
    
    return final_fields
