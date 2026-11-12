def window_minima(values: List[int], width: int) -> List[int]:
    if width < 1 or width > len(values):
        raise ValueError("Invalid input parameters")
    
    return [min(values[i:i+width]) for i in range(len(values)-width+1)]
