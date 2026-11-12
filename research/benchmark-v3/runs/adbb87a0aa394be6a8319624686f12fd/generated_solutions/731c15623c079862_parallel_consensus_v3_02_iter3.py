def rotate_grid(grid):
    if not grid or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("Invalid grid dimensions")
    
    return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]
