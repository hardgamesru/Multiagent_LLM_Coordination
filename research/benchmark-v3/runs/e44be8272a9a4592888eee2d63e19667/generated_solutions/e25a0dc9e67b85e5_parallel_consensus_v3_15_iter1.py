def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    left = list(adjacency.keys())
    n_left = len(left)
    index_of = {v: i for i, v in enumerate(left)}

    right_index: dict[str, int] = {}
    adj: list[list[int]] = [[] for _ in range(n_left)]

    for u, nbrs in adjacency.items():
        i = index_of[u]
        seen: set[str] = set()
        for v in nbrs:
            if v in seen:
                continue
            seen.add(v)
            if v not in right_index:
                right_index[v] = len(right_index)
            adj[i].append(right_index[v])

    m_right = len(right_index)
    match_r: list[int] = [-1] * m_right

    def dfs(u: int, seen: list[bool]) -> bool:
        for v in adj[u]:
            if seen[v]:
                continue
            seen[v] = True
            if match_r[v] == -1 or dfs(match_r[v], seen):
                match_r[v] = u
                return True
        return False

    result = 0
    for u in range(n_left):
        seen = [False] * m_right
        if dfs(u, seen):
            result += 1
    return result
