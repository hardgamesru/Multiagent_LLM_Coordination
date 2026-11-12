def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    from collections import deque

    left = list(adjacency.keys())
    L = len(left)
    index = {u: i for i, u in enumerate(left)}

    adj = [set() for _ in range(L)]
    for u, nbrs in adjacency.items():
        for v in nbrs:
            adj[index[u]].add(v)

    match_r: dict[str, str] = {}

    def bfs():
        dist = [None] * L
        q = deque()
        for u in range(L):
            if match_l[u] is None:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = None
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                w = match_r.get(v)
                if w is None:
                    found = True
                elif dist[w] is None:
                    dist[w] = dist[u] + 1
                    q.append(w)
        return dist, found

    def dfs(u, dist):
        for v in adj[u]:
            w = match_r.get(v)
            if w is None or (dist[w] == dist[u] + 1 and dfs(w, dist)):
                match_l[u] = v
                match_r[v] = left[u]
                return True
        dist[u] = None
        return False

    match_l = [None] * L
    result = 0
    while True:
        dist, found = bfs()
        if not found:
            break
        for u in range(L):
            if match_l[u] is None and dfs(u, dist):
                result += 1
    return result
