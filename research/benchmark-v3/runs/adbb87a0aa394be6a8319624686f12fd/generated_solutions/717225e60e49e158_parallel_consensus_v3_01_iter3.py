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
            # Add previous run to result
            result.append([current_char, count])
            # Start new run with different character
            current_char = char
            count = 1
    
    # Add last run after loop ends
    result.append([current_char, count])
    
    return result
