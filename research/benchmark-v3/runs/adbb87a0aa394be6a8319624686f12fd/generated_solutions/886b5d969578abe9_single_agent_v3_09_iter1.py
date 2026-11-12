from collections import deque

def shortest_distances(edges, source):
    if not edges:
        return {source: 0}
    
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = []
        # Add weighted edge
        graph[u].append((v, w))
    
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    
    queue = deque([source])
    
    while queue:
        current = queue.popleft()
        
        # Check for negative cycles using Bellman-Ford relaxation
        for neighbor, weight in graph.get(current, []):
            new_distance = dist[current] + weight
            
            if new_distance < dist[neighbor]:
                # If relaxing an edge decreases distance,
                # check for negative cycle
                if new_distance < 0:
                    raise ValueError("Negative weight detected")
                
                dist[neighbor] = new_distance
                queue.append(neighbor)
    
    # Set unreachable nodes to None
    result = {node: dist[node] if dist[node] != float('inf') else None for node in graph}
    result[source] = 0  # Source has distance 0
    
    return result
