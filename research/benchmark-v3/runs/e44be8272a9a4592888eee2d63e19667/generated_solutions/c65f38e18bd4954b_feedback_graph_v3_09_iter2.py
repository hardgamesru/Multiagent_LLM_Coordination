from collections import deque

def shortest_distances(edges, source):
    if len(edges) == 0:
        return {source: 0}
    
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    
    dist = {node: float('inf') for node in graph.keys()}
    dist[source] = 0
    
    queue = deque([source])
    
    while queue:
        current = queue.popleft()
        
        # Check for negative weights
        for neighbor, weight in graph.get(current, []):
            new_distance = dist[current] + weight
            
            if new_distance < dist[neighbor]:
                raise ValueError("Negative weight detected")
                
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                queue.append(neighbor)
    
    # Set unreachable nodes to None
    result = {node: dist[node] if dist[node] != float('inf') else None for node in graph.keys()}
    return result
