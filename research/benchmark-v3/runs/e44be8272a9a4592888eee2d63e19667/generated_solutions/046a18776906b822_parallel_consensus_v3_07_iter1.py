def window_minima(values: list[int], width: int) -> list[int]:
    n = len(values)
    if width < 1 or width > n:
        raise ValueError
    result = []
    for i in range(n - width + 1):
        result.append(min(values[i:i+width]))
    return result
