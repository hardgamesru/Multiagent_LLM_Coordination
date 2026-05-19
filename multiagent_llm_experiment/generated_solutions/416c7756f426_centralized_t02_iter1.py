def find_max(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("numbers must not be empty")
    return max(numbers)
