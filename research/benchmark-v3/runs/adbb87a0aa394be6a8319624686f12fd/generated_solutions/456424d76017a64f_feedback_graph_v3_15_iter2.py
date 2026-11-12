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
            
            # Iterate through neighbors of current left vertex
            for neighbor in adjacency[node]:
                # If neighbor is not yet matched, form a new pair
                if neighbor not in matched_right:
                    yield node, neighbor
                    continue
                    
                # If neighbor is already matched, try to "steal" it
                stolen_from = matched_right[neighbor]
                if stolen_from not in visited:
                    queue.append(stolen_from)
    
    # Dictionary tracking which right nodes are paired with left nodes
    matched_right = {}
    
    # Counter for number of successful matches
    match_count = 0
    
    # Process each left vertex
    for left_node in adjacency:
        # Skip if already processed or has no available neighbors
        if left_node in matched_right or len(adjacency[left_node]) == 0:
            continue
            
        # Perform BFS starting from current left vertex
        for left, right in bfs(left_node):
            # Assign current right vertex to new left vertex
            matched_right[right] = left
            match_count += 1
            
    return match_count
