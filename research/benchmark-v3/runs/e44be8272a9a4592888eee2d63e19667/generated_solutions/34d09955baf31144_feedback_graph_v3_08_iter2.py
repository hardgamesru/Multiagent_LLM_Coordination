def build_layers(dependencies: dict[str, list[str]]) -> list[list[str]]:
    deps = {k: set(v) for k, v in dependencies.items()}
    nodes = set(deps) | {n for s in deps.values() for n in s}
    for n in nodes:
        deps.setdefault(n, set())
    in_degree = {n: 0 for n in nodes}
    for k, s in deps.items():
        for v in s:
            in_degree[v] += 1
    result: list[list[str]] = []
    remaining = set(nodes)
    while remaining:
        zero = sorted([n for n in remaining if in_degree[n] == 0])
        if not zero:
            raise ValueError("cycle detected")
        result.append(zero)
        for n in zero:
            remaining.remove(n)
            for m in deps[n]:
                in_degree[m] -= 1
    return result
