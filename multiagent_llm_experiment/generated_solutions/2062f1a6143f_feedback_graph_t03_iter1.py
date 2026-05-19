def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if any(start > end for start, end in intervals):
        raise ValueError("Start of interval cannot be greater than end")
    
    # Сортировка интервалов по началу интервала
    merged = []
    for current in sorted(intervals, key=lambda x: x[0]):
        if not merged or current[0] > merged[-1][1]:
            # Начало нового неперекрывающегося интервала
            merged.append(current)
        else:
            # Расширяем текущий объединённый интервал
            merged[-1] = (merged[-1][0], max(merged[-1][1], current[1]))
    
    return merged
