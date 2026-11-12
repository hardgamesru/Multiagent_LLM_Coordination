def rotate_grid(grid):
    if not all(len(row) == len(grid[0]) for row in grid):
        raise ValueError("All rows must be of equal length")
    
    return [
        [grid[j][i] for j in range(len(grid))]
        for i in range(len(grid[0]))
    ]
