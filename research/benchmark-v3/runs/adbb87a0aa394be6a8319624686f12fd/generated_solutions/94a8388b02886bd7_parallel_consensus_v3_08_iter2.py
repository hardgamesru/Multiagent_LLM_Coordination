def build_layers(dependencies: dict[str, list[str]]) -> list[list[str]]:
    deps = {k: set(v) for k, v in dependencies.items()}
    all_nodes = set(deps.keys())
    for v in deps.values():
        all_nodes.update(v)
    indegree = {node: 0 for node in all_nodes}
    dependents = {node: set() for node in all_nodes}
    for node, ds in deps.items():
        for d in ds:
            indegree[node] += 1
            dependents[d].add(node)
    remaining = set(all_nodes)
    result: list[list[str]] = []
    while remaining:
        layer = sorted([n for n in remaining if indegree[n] == 0])
        if not layer:
            raise ValueError("Cycle detected")
        result.append(layer)
        for n in layer:
            remaining.remove(n)
            for m in dependents[n]:
                indegree[m] -= 1
    return result
