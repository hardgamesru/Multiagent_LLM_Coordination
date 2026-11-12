def encode_runs(text: str) -> list[list]:
    if not text:
        return []
    runs = []
    prev = text[0]
    count = 1
    for ch in text[1:]:
        if ch == prev:
            count += 1
        else:
            runs.append([prev, count])
            prev = ch
            count = 1
    runs.append([prev, count])
    return runs
