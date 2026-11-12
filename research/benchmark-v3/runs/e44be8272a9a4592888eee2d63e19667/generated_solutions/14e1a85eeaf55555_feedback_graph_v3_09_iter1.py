import heapq
from collections import defaultdict

def shortest_distances(edges: list[list], source: str) -> dict:
    for u, v, w in edges:
        if w < 0:
            raise ValueError("Graph contains a negative edge weight.")

    nodes = {source}
    for u, v, _ in edges:
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
            new_d = d + w
            if dist[v] is None or new_d < dist[v]:
                dist[v] = new_d
                heapq.heappush(pq, (new_d, v))

    return dist
