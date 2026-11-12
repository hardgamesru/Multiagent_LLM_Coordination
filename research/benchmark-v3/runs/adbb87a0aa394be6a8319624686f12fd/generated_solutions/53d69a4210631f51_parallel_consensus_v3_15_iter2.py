def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    from collections import deque

    adj = {u: list(set(vs)) for u, vs in adjacency.items()}
    L = list(adj.keys())
    R = {v for vs in adj.values() for v in vs}

    pair_u: dict[str, str | None] = {u: None for u in L}
    pair_v: dict[str, str | None] = {v: None for v in R}
    dist: dict[str, int] = {}

    def bfs() -> bool:
        q = deque()
        for u in L:
            if pair_u[u] is None:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = float('inf')
        found = False
        while q:
            u = q.popleft()
            for v in adj.get(u, ()):
                pu = pair_v[v]
                if pu is None:
                    found = True
                elif dist[pu] == float('inf'):
                    dist[pu] = dist[u] + 1
                    q.append(pu)
        return found

    def dfs(u: str) -> bool:
        for v in adj.get(u, ()):
            pu = pair_v[v]
            if pu is None or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = float('inf')
        return False

    matching = 0
    while bfs():
        for u in L:
            if pair_u[u] is None and dfs(u):
                matching += 1
    return matching
