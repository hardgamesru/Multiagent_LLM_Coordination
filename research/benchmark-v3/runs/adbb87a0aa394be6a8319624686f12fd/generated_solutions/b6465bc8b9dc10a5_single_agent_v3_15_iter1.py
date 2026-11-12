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
    
    n_left = len(adjacency)
    matched = {}
    result = 0
    
    for left_vertex in list(adjacency.keys()):
        if left_vertex not in matched:
            bfs(left_vertex)
            result += 1
            
    return result
