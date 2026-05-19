def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    
    # Проверка на корректность интервалов
    for start, end in intervals:
        if start > end:
            raise ValueError("Invalid interval: start > end")
    
    # Сортировка по началу интервала
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged_intervals = [sorted_intervals[0]]
    
    for current_start, current_end in sorted_intervals[1:]:
        previous_start, previous_end = merged_intervals[-1]
        
        # Проверяем, пересекаются ли текущие и предыдущие интервалы
        if current_start <= previous_end:
            # Интервалы пересекаются, объединяем их
            merged_intervals[-1] = (previous_start, max(previous_end, current_end))
        else:
            # Интервалы не пересекаются, добавляем текущий интервал
            merged_intervals.append((current_start, current_end))
    
    return merged_intervals
