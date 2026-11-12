def rotate_grid(grid):
    if not grid or not all(len(row) == len(grid[0]) for row in grid):
        raise ValueError("Invalid grid")
    
    return [[row[i] for row in reversed(grid)] for i in range(len(grid[0]))]
