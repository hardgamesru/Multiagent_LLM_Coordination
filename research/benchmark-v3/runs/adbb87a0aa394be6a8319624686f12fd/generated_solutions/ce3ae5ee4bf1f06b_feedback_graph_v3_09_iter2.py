from collections import deque

def shortest_distances(edges, source):
    if not isinstance(source, str):
        raise TypeError("Source must be a string")
    
    graph = {}
    for u, v, w in edges:
        if not isinstance(u, str) or not isinstance(v, str):
            raise TypeError("Node names must be strings")
        
        if u not in graph:
            graph[u] = []
        # Check for negative weights
        if w < 0:
            raise ValueError("Negative weight found")
            
        graph[u].append((v, w))
    
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    
    queue = deque()
    queue.append(source)
    
    while queue:
        current = queue.popleft()
        
        # Avoid revisiting nodes that are already processed
        if dist[current] == float('inf'):
            continue
            
        for neighbor, weight in graph.get(current, []):
            new_distance = dist[current] + weight
            
            # Update distance if shorter path found
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                queue.append(neighbor)
                
    # Replace infinity with None for unreachable nodes
    return {node: None if d == float('inf') else d for node, d in dist.items()}
