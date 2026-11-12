def rotate_grid(grid: list[list[int]]) -> list[list[int]]:
    if not grid:
        return []
    row_len = len(grid[0])
    if row_len == 0:
        raise ValueError
    for row in grid:
        if len(row) != row_len:
            raise ValueError
    return [[grid[r][c] for r in range(len(grid) - 1, -1, -1)] for c in range(row_len)]
