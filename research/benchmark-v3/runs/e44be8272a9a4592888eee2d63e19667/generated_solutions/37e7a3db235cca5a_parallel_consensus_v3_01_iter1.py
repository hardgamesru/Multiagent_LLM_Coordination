def encode_runs(text: str) -> list[list]:
    if not text:
        return []
    
    result = []
    current_char = text[0]
    count = 1
    
    for char in text[1:]:
        if char == current_char:
            count += 1
        else:
            # Append previous run with its count
            result.append([current_char, count])
            # Start new run
            current_char = char
            count = 1
    
    # Add last run
    result.append([current_char, count])
    
    return result
