def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    left = list(adjacency.keys())
    right = {v for nbrs in adjacency.values() for v in nbrs}
    match_r: dict[str, str | None] = {v: None for v in right}

    def dfs(u: str, seen: set[str]) -> bool:
        for v in adjacency.get(u, []):
            if v in seen:
                continue
            seen.add(v)
            if match_r[v] is None or dfs(match_r[v], seen):
                match_r[v] = u
                return True
        return False

    result = 0
    for u in left:
        if dfs(u, set()):
            result += 1
    return result
