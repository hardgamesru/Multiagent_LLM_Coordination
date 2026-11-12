def build_layers(dependencies):
    deps = {k: set(v) for k, v in dependencies.items()}
    all_nodes = set(deps) | {d for v in deps.values() for d in v}
    for n in all_nodes:
        deps.setdefault(n, set())
    in_degree = {n: 0 for n in all_nodes}
    adj = {n: set() for n in all_nodes}
    for n, ds in deps.items():
        for d in ds:
            if n not in adj[d]:
                adj[d].add(n)
                in_degree[n] += 1
    layers = []
    remaining = set(all_nodes)
    while remaining:
        ready = sorted([n for n in remaining if in_degree[n] == 0])
        if not ready:
            raise ValueError("Cycle detected")
        layers.append(ready)
        for n in ready:
            remaining.remove(n)
            for m in adj[n]:
                in_degree[m] -= 1
    return layers
