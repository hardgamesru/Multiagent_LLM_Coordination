def build_layers(dependencies: dict[str, list[str]]) -> list[list[str]]:
    deps = {k: set(v) for k, v in dependencies.items()}
    nodes = set(deps)
    for v in deps.values():
        nodes.update(v)
    graph = {n: set() for n in nodes}
    for u, vs in deps.items():
        for v in vs:
            graph[v].add(u)
    indeg = {n: len(deps.get(n, set())) for n in nodes}
    result: list[list[str]] = []
    remaining = set(nodes)
    while remaining:
        ready = sorted([n for n in remaining if indeg[n] == 0])
        if not ready:
            raise ValueError("Cycle detected")
        result.append(ready)
        for n in ready:
            remaining.remove(n)
            for m in graph[n]:
                indeg[m] -= 1
    return result
