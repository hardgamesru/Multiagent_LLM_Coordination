def find_max(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("Список пуст")
    return max(numbers)
