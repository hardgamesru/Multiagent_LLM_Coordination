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
            # Добавляем предыдущий пробег с правильным регистром
            result.append([current_char, count])
            current_char = char
            count = 1
    
    # Добавляем последний пробег
    result.append([current_char, count])
    
    return result
