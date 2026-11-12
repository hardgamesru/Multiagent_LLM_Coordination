from typing import List, Dict, Optional

def shortest_distances(edges: List[List[str]], source: str) -> Optional[Dict[str, int]]:
    if not edges:
        return {source: 0}
    
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, int(w)))
    
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    
    # Relaxation loop
    for _ in range(len(graph)):
        updated = False
        for u in graph:
            for v, w in graph[u]:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
        
        # Detect negative cycles
        if not updated:
            break
    
    else:
        # Check for negative-weight cycles
        for u in graph:
            for _, w in graph[u]:
                if dist[u] != float('inf') and dist[u] + w < dist[u]:
                    raise ValueError("Graph contains negative-weight cycle")
    
    result = {node: dist.get(node, None) for node in graph}
    result[source] = 0
    return result
