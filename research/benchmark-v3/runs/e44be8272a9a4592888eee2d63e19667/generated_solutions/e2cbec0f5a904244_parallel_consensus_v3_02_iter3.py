def rotate_grid(grid):
    if not all(len(row) == len(grid[0]) for row in grid):
        raise ValueError("All rows must be of equal length")
    
    return [list(row) for row in zip(*reversed(grid))]
