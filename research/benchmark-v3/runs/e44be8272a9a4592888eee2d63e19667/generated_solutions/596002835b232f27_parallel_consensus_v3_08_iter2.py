def build_layers(dependencies: dict[str, list[str]]) -> list[list[str]]:
    deps = {k: set(v) for k, v in dependencies.items()}
    nodes = set(deps) | {n for v in deps.values() for n in v}
    indeg = {n: 0 for n in nodes}
    adj = {n: set() for n in nodes}
    for u, ds in deps.items():
        for v in ds:
            if u not in adj[v]:
                adj[v].add(u)
                indeg[u] += 1
    layers: list[list[str]] = []
    remaining = set(nodes)
    while remaining:
        ready = sorted([n for n in remaining if indeg[n] == 0])
        if not ready:
            raise ValueError("cycle")
        layers.append(ready)
        for n in ready:
            remaining.remove(n)
            for m in adj[n]:
                indeg[m] -= 1
    return layers
