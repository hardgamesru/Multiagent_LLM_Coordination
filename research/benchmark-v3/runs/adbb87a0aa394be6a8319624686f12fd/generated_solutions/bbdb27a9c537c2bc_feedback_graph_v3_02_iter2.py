def rotate_grid(grid):
    if not grid or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError()
    
    return [[row[col] for row in reversed(grid)] for col in range(len(grid[0]))]
