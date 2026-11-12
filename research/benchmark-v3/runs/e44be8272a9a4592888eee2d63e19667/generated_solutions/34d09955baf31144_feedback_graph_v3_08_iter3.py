def build_layers(dependencies: dict[str, list[str]]) -> list[list[str]]:
    deps = {k: set(v) for k, v in dependencies.items()}
    nodes = set(deps)
    for v in deps.values():
        nodes.update(v)
    for n in nodes:
        deps.setdefault(n, set())
    indeg = {n: 0 for n in nodes}
    for u, vs in deps.items():
        for v in vs:
            indeg[v] += 1
    layers: list[list[str]] = []
    remaining = set(nodes)
    while remaining:
        ready = sorted([n for n in remaining if indeg[n] == 0])
        if not ready:
            raise ValueError("cycle")
        layers.append(ready)
        for n in ready:
            remaining.remove(n)
            for m in deps[n]:
                indeg[m] -= 1
    return layers
