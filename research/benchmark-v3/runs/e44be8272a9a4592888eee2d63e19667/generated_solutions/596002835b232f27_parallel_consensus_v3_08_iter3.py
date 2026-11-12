def build_layers(dependencies):
    deps = {k: set(v) for k, v in dependencies.items()}
    nodes = set(deps) | {d for s in deps.values() for d in s}
    for n in nodes:
        deps.setdefault(n, set())
    indeg = {n: 0 for n in nodes}
    for n, s in deps.items():
        for d in s:
            indeg[d] += 1
    layers = []
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
