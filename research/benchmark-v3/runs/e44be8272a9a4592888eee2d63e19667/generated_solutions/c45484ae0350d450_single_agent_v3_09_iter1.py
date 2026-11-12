import heapq
from collections import defaultdict

def shortest_distances(edges: list[list], source: str) -> dict:
    nodes = {source}
    for u, v, w in edges:
        if w < 0:
            raise ValueError("Negative weight")
        nodes.add(u)
        nodes.add(v)

    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = {node: None for node in nodes}
    dist[source] = 0
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
