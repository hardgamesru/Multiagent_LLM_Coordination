from collections import deque
import sys

def shortest_distances(edges: list[list], source: str) -> dict:
    if not edges:
        return {source: 0}
    
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    
    queue = deque([source])
    
    while queue:
        current = queue.popleft()
        
        # Check for negative weights using Bellman-Ford algorithm
        for neighbor, weight in graph.get(current, []):
            new_dist = dist[current] + weight
            
            if new_dist < dist[neighbor]:
                if dist[neighbor] == float('inf'):
                    # First time visiting neighbor
                    dist[neighbor] = new_dist
                    queue.append(neighbor)
                else:
                    # Negative cycle detected
                    raise ValueError("Negative weight found")
    
    # Convert infinities to None
    result = {node: None if d == float('inf') else d for node, d in dist.items()}
    result[source] = 0
    return result
