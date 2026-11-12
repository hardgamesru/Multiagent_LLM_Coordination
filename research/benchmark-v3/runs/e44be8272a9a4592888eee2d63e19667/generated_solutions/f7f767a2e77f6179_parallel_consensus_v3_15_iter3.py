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
                if neighbor not in visited:
                    yield neighbor
                    queue.append(neighbor)
    
    max_match = 0
    seen_left = set()
    
    for left_node in adjacency.keys():
        if left_node not in seen_left:
            # Track which right nodes were used from current left node
            used_rights = set()
            
            # BFS to find unmatched right nodes connected to current left node
            for right_node in bfs(left_node):
                if right_node not in used_rights:
                    max_match += 1
                    used_rights.add(right_node)
                    # Mark both sides as seen to prevent reusing them
                    seen_left.add(left_node)
                    seen_left.update(adjacency[right_node])
    
    return max_match
