def rotate_grid(grid):
    if not grid or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("Invalid grid dimensions")
    
    return [list(row) for row in zip(*reversed(grid))]
