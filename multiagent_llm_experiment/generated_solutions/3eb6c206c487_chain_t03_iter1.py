def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # Проверка корректности входных данных
    for start, end in intervals:
        if start > end:
            raise ValueError("Invalid interval")
    
    # Сортировка интервалов по началу
    sorted_intervals = sorted(intervals)
    
    merged = []
    for current_interval in sorted_intervals:
        # Если результат пустой или текущий интервал не пересекается с последним,
        # добавляем его как новый элемент
        if not merged or merged[-1][1] < current_interval[0]:
            merged.append(current_interval)
        else:
            # Иначе расширяем последний интервал до максимума текущего конца
            merged[-1] = (merged[-1][0], max(merged[-1][1], current_interval[1]))
    
    return merged
