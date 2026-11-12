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
            
            for neighbor in adjacency.get(node, []):
                if neighbor not in matched or bfs(matched[neighbor]):
                    matched[node] = neighbor
                    return True
        
        return False
    
    # Initialize matching dictionary
    matched = {}
    
    # Try each vertex as a starting point
    for start in adjacency.keys():
        bfs(start)
    
    # Count number of matches
    return len(matched)
