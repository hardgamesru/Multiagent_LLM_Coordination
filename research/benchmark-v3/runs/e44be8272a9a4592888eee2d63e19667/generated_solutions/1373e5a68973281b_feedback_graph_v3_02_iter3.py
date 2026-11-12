def rotate_grid(grid):
    if not grid or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError()
    
    return [[row[i] for row in reversed(grid)] for i in range(len(grid[0]))]
