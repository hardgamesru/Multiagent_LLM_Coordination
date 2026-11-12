from collections import deque

def maximum_matching(adjacency):
    def bfs(start):
        queue = deque([start])
        visited = set()
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
    
    # Initialize matching dictionary
    matched = {}
    max_match = 0
    
    # Process each vertex as a starting point
    for start in adjacency:
        # Reset visited state for new search
        visited = set()
        # Try to expand matching from current vertex
        if bfs(start):
            max_match += 1
            
    return max_match
