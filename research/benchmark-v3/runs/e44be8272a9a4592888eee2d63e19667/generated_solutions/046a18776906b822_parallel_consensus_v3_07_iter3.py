def window_minima(values: list[int], width: int) -> list[int]:
    if width < 1 or width > len(values):
        raise ValueError
    return [min(values[i:i+width]) for i in range(len(values) - width + 1)]
