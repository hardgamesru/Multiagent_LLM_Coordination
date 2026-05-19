def parse_csv_line(line: str) -> list[str]:
    import re
    result = []
    quote_mode = False
    current_field = ''
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            # Start or end of quoted field
            if not quote_mode:
                quote_mode = True
            else:
                # Escape sequence: ""
                if i + 1 < len(line) and line[i+1] == '"':
                    current_field += '"'
                    i += 2
                else:
                    quote_mode = False
        elif char == ',':
            # Field separator outside quotes
            if not quote_mode:
                result.append(current_field.strip())
                current_field = ''
        else:
            # Accumulate characters
            current_field += char
        
        i += 1
    
    # Append last field
    result.append(current_field.strip())
    
    return [field for field in result if field]
