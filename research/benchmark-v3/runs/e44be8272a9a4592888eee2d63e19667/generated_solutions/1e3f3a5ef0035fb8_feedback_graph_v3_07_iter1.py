from typing import List

def window_minima(values: List[int], width: int) -> List[int]:
    if width > len(values):
        raise ValueError("Window width exceeds list length")
    
    # Используем срезы для избежания мутации входного списка
    return [min(values[i:i + width]) for i in range(len(values) - width + 1)]
