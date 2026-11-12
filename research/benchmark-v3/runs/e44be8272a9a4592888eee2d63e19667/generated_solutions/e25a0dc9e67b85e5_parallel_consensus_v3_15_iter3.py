def maximum_matching(adjacency: dict[str, list[str]]) -> int:
    left = list(adjacency.keys())
    right = {v for nbrs in adjacency.values() for v in nbrs}
    r_index = {v: i for i, v in enumerate(right)}
    R = len(right)
    adj_bits = [0] * len(left)
    for i, u in enumerate(left):
        bits = 0
        for v in adjacency[u]:
            j = r_index[v]
            bits |= 1 << j
        adj_bits[i] = bits

    match_r = [-1] * R

    def dfs(u_idx: int, seen: int) -> bool:
        neigh = adj_bits[u_idx]
        while neigh:
            lsb = neigh & -neigh
            v = lsb.bit_length() - 1
            neigh ^= lsb
            if (seen >> v) & 1:
                continue
            seen |= 1 << v
            w = match_r[v]
            if w == -1 or dfs(w, seen):
                match_r[v] = u_idx
                return True
        return False

    result = 0
    for u_idx in range(len(left)):
        if dfs(u_idx, 0):
            result += 1
    return result
