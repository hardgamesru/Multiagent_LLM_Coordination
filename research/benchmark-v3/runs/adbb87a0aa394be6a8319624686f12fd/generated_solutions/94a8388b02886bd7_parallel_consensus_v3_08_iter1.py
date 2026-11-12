def build_layers(dependencies: dict[str, list[str]]) -> list[list[str]]:
    deps_copy = {k: list(v) for k, v in dependencies.items()}
    all_nodes = set(deps_copy.keys())
    for v in deps_copy.values():
        all_nodes.update(v)
    in_degree = {node: 0 for node in all_nodes}
    reverse_graph = {node: [] for node in all_nodes}
    for node, ds in deps_copy.items():
        for d in set(ds):
            in_degree[node] += 1
            reverse_graph[d].append(node)
    layers = []
    remaining = set(all_nodes)
    while remaining:
        zero = sorted([n for n in remaining if in_degree[n] == 0])
        if not zero:
            raise ValueError("Cycle detected")
        layers.append(zero)
        remaining.difference_update(zero)
        for n in zero:
            for dependent in reverse_graph[n]:
                in_degree[dependent] -= 1
    return layers
