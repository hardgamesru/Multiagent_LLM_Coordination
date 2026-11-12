def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if any(start > end for start, end in intervals):
        raise ValueError("Interval start cannot be greater than end")
    
    # Сортировка интервалов по началу интервала
    merged = []
    for interval in sorted(intervals, key=lambda x: x[0]):
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            # Обновляем конец последнего объединенного интервала,
            # если текущий интервал перекрывает его
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
    
    return merged
