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
    
    # BFS queue stores (node, current_distance)
    q = deque([(source, 0)])
    
    while q:
        curr_node, curr_dist = q.popleft()
        
        # Check for negative weights
        if curr_dist >= dist[curr_node]:
            continue
            
        for neighbor, weight in graph.get(curr_node, []):
            new_dist = curr_dist + weight
            
            # Update distance if shorter path found
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                q.append((neighbor, new_dist))
                
    # Convert infinities to None
    result = {k: None if v == float('inf') else v for k, v in dist.items()}
    result[source] = 0
    
    return result
