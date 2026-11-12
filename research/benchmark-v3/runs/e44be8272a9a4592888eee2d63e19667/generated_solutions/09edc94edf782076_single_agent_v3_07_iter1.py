def window_minima(values: list[int], width: int) -> list[int]:
    if not (1 <= width <= len(values)):
        raise ValueError
    return [min(values[i:i+width]) for i in range(len(values) - width + 1)]
