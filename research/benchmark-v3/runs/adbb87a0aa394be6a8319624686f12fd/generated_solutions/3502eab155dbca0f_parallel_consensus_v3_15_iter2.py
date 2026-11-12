from collections import deque

def maximum_matching(adjacency):
    def bfs(start):
        visited = set()
        queue = deque([start])
        while queue:
            u = queue.popleft()
            if u in visited:
                continue
            visited.add(u)
            for v in adjacency.get(u, []):
                if v not in matched_to or bfs(matched_to[v]):
                    matched_to[v] = u
                    return True
            queue.extend(adjacent_vertices - visited)
        return False
    
    # Initialize matching dictionary
    matched_to = {}
    max_match = 0
    
    # List of all left-side vertices
    left_vertices = list(adjacency.keys())
    
    # Process each vertex from left side
    for start_vertex in left_vertices:
        adjacent_vertices = set(adjacency.get(start_vertex, []))
        
        # Skip if already matched or no unvisited neighbors
        if start_vertex in matched_to or not adjacent_vertices:
            continue
            
        # Perform BFS to find augmenting path
        if bfs(start_vertex):
            max_match += 1
    
    return max_match
