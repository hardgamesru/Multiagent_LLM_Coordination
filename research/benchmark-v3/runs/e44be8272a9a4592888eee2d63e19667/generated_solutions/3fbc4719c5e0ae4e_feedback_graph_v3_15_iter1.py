from collections import deque

def bfs(adjacency: dict[str, list[str]], src: str, visited_left: set[str], matched_right: set[str]) -> bool:
    queue = deque([src])
    while queue:
        u = queue.popleft()
        if u in visited_left:
            continue
        visited_left.add(u)
        for v in adjacency.get(u, []):
            if v not in matched_right:
                return True
            next_u = matched_right[v]
            if next_u not in visited_left:
                queue.append(next_u)
    return False

def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    left_vertices = set(adjacency.keys())
    right_vertices = set().union(*adjacency.values())
    
    # Initialize matching with empty sets
    matched_left = set()
    matched_right = {}
    
    # Track which left vertices were visited during BFS
    visited_left = set()
    
    # Iterate through unmatched left vertices
    for u in left_vertices:
        if u not in visited_left and u not in matched_left:
            # Try to find augmenting path using BFS
            found = False
            for _ in range(len(left_vertices)):
                if found:
                    break
                # Reset visited left vertices for each iteration
                visited_left.clear()
                found = bfs(adjacency, u, visited_left, matched_right)
        
            # Add to matching if augmenting path is found
            if found:
                matched_left.add(u)
                matched_right[u] = None
    
    return len(matched_left)
