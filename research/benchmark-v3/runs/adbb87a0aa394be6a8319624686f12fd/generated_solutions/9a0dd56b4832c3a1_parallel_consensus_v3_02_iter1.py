def rotate_grid(grid: list[list[int]]) -> list[list[int]]:
    if not grid:
        return []
    row_len = len(grid[0])
    if row_len == 0:
        raise ValueError("Empty row")
    for row in grid:
        if len(row) != row_len:
            raise ValueError("Unequal row lengths")
    return [list(reversed(col)) for col in zip(*grid)]
