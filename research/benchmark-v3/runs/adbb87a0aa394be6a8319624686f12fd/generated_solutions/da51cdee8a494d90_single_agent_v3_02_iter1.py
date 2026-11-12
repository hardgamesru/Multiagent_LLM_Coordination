def rotate_grid(grid):
    if not grid or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("Invalid grid")
    
    return [[grid[i][j] for i in range(len(grid)-1,-1,-1)] for j in range(len(grid[0]))]
