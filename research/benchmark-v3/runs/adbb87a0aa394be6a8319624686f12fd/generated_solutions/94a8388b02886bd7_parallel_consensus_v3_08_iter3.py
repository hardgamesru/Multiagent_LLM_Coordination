def build_layers(dependencies: dict[str, list[str]]) -> list[list[str]]:
    deps = {k: set(v) for k, v in dependencies.items()}
    all_nodes = set(deps.keys())
    for v in deps.values():
        all_nodes.update(v)
    in_degree = {node: 0 for node in all_nodes}
    for node, ds in deps.items():
        in_degree[node] = len(ds)
    reverse_graph = {node: [] for node in all_nodes}
    for node, ds in deps.items():
        for d in ds:
            reverse_graph[d].append(node)
    result: list[list[str]] = []
    remaining = set(all_nodes)
    while remaining:
        zero = sorted([n for n in remaining if in_degree[n] == 0])
        if not zero:
            raise ValueError("Cycle detected")
        result.append(zero)
        for n in zero:
            remaining.remove(n)
            for dependent in reverse_graph[n]:
                in_degree[dependent] -= 1
    return result
