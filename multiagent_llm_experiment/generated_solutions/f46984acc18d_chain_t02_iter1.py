def parse_csv_line(line: str) -> list[str]:
    result = []
    i, n = 0, len(line)
    
    def consume_quoted_field():
        nonlocal i
        s = ""
        i += 1 # skip opening "
        while i < n and (ch := line[i]) != '"':
            if ch == '"' and i + 1 < n and line[i+1] == '"': 
                s += '"'  
                i += 2  # Skip doubled quotes
            else:
                s += ch
                i += 1
        i += 1  # skip closing "
        return s
        
    while i < n:
        start = i
        while i < n and line[i] != ',' and line[i] != '"':
            i += 1
            
        if i >= n or line[i] == ',':
            result.append(line[start:i])
            i += 1
        elif line[i] == '"':
            result.append(consume_quoted_field())
    
    return result
