def window_minima(values: list[int], width: int) -> list[int]:
    if width < 1 or width > len(values):
        raise ValueError
    result = []
    for i in range(len(values) - width + 1):
        result.append(min(values[i:i+width]))
    return result
