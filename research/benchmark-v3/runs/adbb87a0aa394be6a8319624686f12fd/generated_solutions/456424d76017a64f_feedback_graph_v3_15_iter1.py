from collections import deque

def maximum_matching(adjacency):
    def bfs(start):
        visited = set()
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            # Explore neighbors that haven't been matched yet
            for neighbor in adjacency[node]:
                if neighbor not in matched or bfs(matched[neighbor]):
                    matched[neighbor] = node
                    return True
            queue.append(node)
        return False
    
    # Track which nodes from right side are matched
    matched = {}
    max_size = 0
    
    # Try each vertex as starting point
    for left_vertex in adjacency:
        # Reset visited state for new search
        visited = set()
        # Find augmenting path using BFS
        if bfs(left_vertex):
            max_size += 1
    
    return max_size
