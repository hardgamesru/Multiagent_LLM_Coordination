def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    left = list(adjacency.keys())
    right_set = set(v for nbrs in adjacency.values() for v in nbrs)
    right = list(right_set)
    r_index = {v: i for i, v in enumerate(right)}

    nL, nR = len(left), len(right)
    adj = [[False] * nR for _ in range(nL)]
    for i, u in enumerate(left):
        for v in adjacency[u]:
            j = r_index[v]
            adj[i][j] = True

    matchR = [-1] * nR

    def dfs(u: int, seen: list[bool]) -> bool:
        for v in range(nR):
            if adj[u][v] and not seen[v]:
                seen[v] = True
                if matchR[v] == -1 or dfs(matchR[v], seen):
                    matchR[v] = u
                    return True
        return False

    result = 0
    for u in range(nL):
        seen = [False] * nR
        if dfs(u, seen):
            result += 1
    return result
