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
            # Add previous run to result with correct case
            result.append([current_char.upper(), count])
            
            # Start new run with current character
            current_char = char
            count = 1
    
    # Add last run to result
    result.append([current_char.upper(), count])
    
    return result
