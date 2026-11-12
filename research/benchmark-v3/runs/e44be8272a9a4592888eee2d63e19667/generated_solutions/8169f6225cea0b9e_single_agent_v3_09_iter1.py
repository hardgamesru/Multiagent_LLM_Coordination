from collections import deque
import sys

def shortest_distances(edges, source):
    if len(edges) == 0:
        return {source: 0}
    
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    
    queue = deque()
    queue.append(source)
    
    while queue:
        current = queue.popleft()
        
        # Check for negative weights
        for neighbor, weight in graph.get(current, []):
            new_dist = dist[current] + weight
            
            if new_dist < dist[neighbor]:
                raise ValueError("Negative weight detected")
                
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                queue.append(neighbor)
    
    # Set unreachable distances to None
    for node in dist:
        if dist[node] == float('inf'):
            dist[node] = None
    
    return dist
