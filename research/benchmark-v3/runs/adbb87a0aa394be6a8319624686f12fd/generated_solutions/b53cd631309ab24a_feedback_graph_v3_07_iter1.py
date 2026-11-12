def window_minima(values: list[int], width: int) -> list[int]:
    n = len(values)
    if width < 1 or width > n:
        raise ValueError("width must satisfy 1 <= width <= len(values)")
    return [min(values[i:i+width]) for i in range(n - width + 1)]
