def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    # Build adjacency with unique edges, without mutating input
    adj = {u: list(set(vs)) for u, vs in adjacency.items()}

    # Collect all right-side vertices
    right_vertices = set()
    for vs in adj.values():
        right_vertices.update(vs)

    # Map right vertices to indices
    r_index = {v: i for i, v in enumerate(right_vertices)}
    R = len(r_index)

    # Build adjacency lists as lists of indices
    adj_idx = {u: [r_index[v] for v in vs] for u, vs in adj.items()}

    # match_r[i] = left vertex matched to right i, or None
    match_r: list[str | None] = [None] * R

    def dfs(u: str, seen: set[int]) -> bool:
        for i in adj_idx.get(u, ()):
            if i in seen:
                continue
            seen.add(i)
            if match_r[i] is None or dfs(match_r[i], seen):
                match_r[i] = u
                return True
        return False

    result = 0
    for u in adj:
        if dfs(u, set()):
            result += 1
    return result
