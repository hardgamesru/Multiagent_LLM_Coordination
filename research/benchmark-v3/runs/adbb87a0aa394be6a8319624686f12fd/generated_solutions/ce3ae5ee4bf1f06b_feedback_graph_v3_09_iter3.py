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
    
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    
    queue = deque()
    queue.append(source)
    
    while queue:
        current_node = queue.popleft()
        
        # If no neighbors, continue
        if not graph.get(current_node):
            continue
            
        for neighbor, weight in graph[current_node]:
            new_distance = distances[current_node] + weight
            
            # Update distance if shorter path found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                queue.append(neighbor)
                
    # Replace infinity with None for unreachable nodes
    return {node: dist if dist != float('inf') else None for node, dist in distances.items()}
