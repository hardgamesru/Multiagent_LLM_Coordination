import heapq
from collections import defaultdict

def shortest_distances(edges: list[list], source: str) -> dict:
    for e in edges:
        if len(e) != 3 or not isinstance(e[2], int) or e[2] < 0:
            raise ValueError
    adj = defaultdict(list)
    nodes = {source}
    for u, v, w in edges:
        adj[u].append((v, w))
        nodes.add(u)
        nodes.add(v)
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
