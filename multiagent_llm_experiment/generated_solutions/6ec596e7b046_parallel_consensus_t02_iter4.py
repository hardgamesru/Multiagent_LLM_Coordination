def find_max(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("Список чисел не должен быть пустым")
    return max(numbers)
