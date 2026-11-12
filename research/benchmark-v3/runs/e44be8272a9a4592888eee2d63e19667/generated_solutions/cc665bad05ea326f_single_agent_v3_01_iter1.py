def encode_runs(text: str) -> list[list]:
    if not text:
        return []
    result = []
    current_char = text[0]
    count = 1
    for ch in text[1:]:
        if ch == current_char:
            count += 1
        else:
            result.append([current_char, count])
            current_char = ch
            count = 1
    result.append([current_char, count])
    return result
