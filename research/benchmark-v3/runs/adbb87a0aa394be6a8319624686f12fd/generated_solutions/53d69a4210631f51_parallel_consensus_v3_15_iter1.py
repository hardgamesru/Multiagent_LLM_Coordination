def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    left = list(adjacency.keys())
    n_left = len(left)
    index = {v: i for i, v in enumerate(left)}

    adj_sets: list[set[str]] = [set(adjacency[v]) for v in left]

    match_r: dict[str, int] = {}

    def dfs(u: int, seen: set[str]) -> bool:
        for v in adj_sets[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in match_r or dfs(match_r[v], seen):
                match_r[v] = u
                return True
        return False

    result = 0
    for u in range(n_left):
        if dfs(u, set()):
            result += 1
    return result
