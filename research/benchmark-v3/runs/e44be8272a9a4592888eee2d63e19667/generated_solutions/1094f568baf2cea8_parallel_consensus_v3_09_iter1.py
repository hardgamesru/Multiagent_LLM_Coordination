import heapq
from typing import List, Dict, Optional

def shortest_distances(edges: List[List], source: str) -> Dict[str, Optional[int]]:
    # Validate weights
    for e in edges:
        if len(e) != 3:
            continue
        if e[2] < 0:
            raise ValueError("Negative weight")

    # Collect vertices
    vertices = {source}
    for u, v, _ in edges:
        vertices.add(u)
        vertices.add(v)

    # Build adjacency list
    adj: Dict[str, List[tuple[str, int]]] = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))

    # Dijkstra
    dist: Dict[str, Optional[int]] = {v: None for v in vertices}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if dist[u] is not None and d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
