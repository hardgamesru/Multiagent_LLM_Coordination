def encode_runs(text: str) -> list[list]:
    if not text:
        return []
    result = []
    prev = text[0]
    count = 1
    for ch in text[1:]:
        if ch == prev:
            count += 1
        else:
            result.append([prev, count])
            prev = ch
            count = 1
    result.append([prev, count])
    return result
