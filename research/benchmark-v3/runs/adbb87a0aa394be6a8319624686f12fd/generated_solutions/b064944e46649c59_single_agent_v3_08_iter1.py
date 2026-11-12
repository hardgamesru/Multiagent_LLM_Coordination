def build_layers(dependencies):
    deps = {k: set(v) for k, v in dependencies.items()}
    all_nodes = set(deps) | {d for v in deps.values() for d in v}
    for n in all_nodes:
        deps.setdefault(n, set())
    in_degree = {n: 0 for n in all_nodes}
    for n, ds in deps.items():
        for d in ds:
            in_degree[d] += 1
    ready = sorted([n for n, d in in_degree.items() if d == 0])
    layers = []
    while ready:
        layers.append(ready)
        next_ready = []
        for n in ready:
            for m in deps[n]:
                in_degree[m] -= 1
                if in_degree[m] == 0:
                    next_ready.append(m)
        ready = sorted(set(next_ready))
    if any(d > 0 for d in in_degree.values()):
        raise ValueError("Cycle detected")
    return layers
