from typing import List, Dict, Optional

def shortest_distances(edges: List[List[str]], source: str) -> Optional[Dict[str, int]]:
    if any(len(e) != 3 for e in edges):
        raise ValueError("Each edge must have exactly three elements")
    
    graph = {}
    for u, v, w in edges:
        if w < 0:
            raise ValueError("Negative weights are not allowed")
        
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    
    # Relaxation loop
    for _ in range(len(graph)):
        updated = False
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
        
        # Check for negative cycles
        if not updated:
            break
    
    else:
        # Second pass to detect negative cycles
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    return None
    
    # Convert infinities back to None
    result = {k: None if v == float('inf') else v for k, v in dist.items()}
    result[source] = 0
    return result
