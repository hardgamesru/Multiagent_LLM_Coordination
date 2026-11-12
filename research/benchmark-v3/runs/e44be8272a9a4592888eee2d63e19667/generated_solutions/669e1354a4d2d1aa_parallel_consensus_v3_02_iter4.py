def rotate_grid(grid: list[list[int]]) -> list[list[int]]:
    if not grid:
        return []
    if not all(grid) or len({len(r) for r in grid}) != 1:
        raise ValueError
    return [list(reversed(col)) for col in zip(*grid)]
