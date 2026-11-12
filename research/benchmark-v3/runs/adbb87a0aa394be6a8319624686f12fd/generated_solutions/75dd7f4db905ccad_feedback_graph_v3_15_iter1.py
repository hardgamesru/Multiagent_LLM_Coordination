def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    from collections import deque

    # Build unique adjacency and collect right-side vertices
    adj_unique: dict[str, set[str]] = {}
    right_vertices: set[str] = set()
    for u, nbrs in adjacency.items():
        uniq = set(nbrs)
        adj_unique[u] = uniq
        right_vertices.update(uniq)

    # Map right vertices to indices
    right_list = list(right_vertices)
    r_index = {v: i for i, v in enumerate(right_list)}
    R = len(right_list)

    # Pairings: None means free
    pair_u: dict[str, str | None] = {u: None for u in adj_unique}
    pair_v: list[str | None] = [None] * R

    def bfs() -> dict[str, int]:
        dist: dict[str, int] = {}
        q = deque()
        for u in adj_unique:
            if pair_u[u] is None:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = -1
        found = False
        while q:
            u = q.popleft()
            for v in adj_unique[u]:
                i = r_index[v]
                pu = pair_v[i]
                if pu is None:
                    found = True
                elif dist[pu] == -1:
                    dist[pu] = dist[u] + 1
                    q.append(pu)
        return dist if found else {}

    def dfs(u: str, dist: dict[str, int]) -> bool:
        for v in adj_unique[u]:
            i = r_index[v]
            pu = pair_v[i]
            if pu is None or (dist[pu] == dist[u] + 1 and dfs(pu, dist)):
                pair_u[u] = v
                pair_v[i] = u
                return True
        dist[u] = -1
        return False

    matching = 0
    while True:
        dist = bfs()
        if not dist:
            break
        for u in adj_unique:
            if pair_u[u] is None and dfs(u, dist):
                matching += 1
    return matching
