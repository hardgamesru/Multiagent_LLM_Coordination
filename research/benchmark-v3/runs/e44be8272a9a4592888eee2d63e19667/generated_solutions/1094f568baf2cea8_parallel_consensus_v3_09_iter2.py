def shortest_distances(edges, source):
    for e in edges:
        if e[2] < 0:
            raise ValueError
    nodes = {source}
    for u, v, _ in edges:
        nodes.add(u)
        nodes.add(v)
    dist = {n: None for n in nodes}
    dist[source] = 0
    import heapq
    pq = [(0, source)]
    adj = {n: [] for n in nodes}
    for u, v, w in edges:
        adj[u].append((v, w))
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
