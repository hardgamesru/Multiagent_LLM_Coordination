from typing import List, Dict, Optional

def shortest_distances(edges: List[List[str]], source: str) -> Optional[Dict[str, int]]:
    if not edges:
        return {source: 0}
    
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    
    dist = {node: float('inf') for node in graph.keys()}
    dist[source] = 0
    
    # Relaxation loop
    for _ in range(len(graph)):
        updated = False
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
        
        # Early termination if no updates
        if not updated:
            break
    
    else:
        # Check for negative cycles
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    raise ValueError("Negative-weight cycle detected")
    
    result = {node: dist.get(node, None) for node in graph.keys()}
    result[source] = 0  # Ensure source has distance 0
    return result
