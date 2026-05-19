def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    nodes = set(dependencies)
    for deps in dependencies.values():
        nodes.update(deps)
    outgoing = {node: set() for node in nodes}
    indegree = {node: 0 for node in nodes}
    for task, deps in dependencies.items():
        for dep in deps:
            outgoing.setdefault(dep, set()).add(task)
            indegree[task] = indegree.get(task, 0) + 1
            indegree.setdefault(dep, 0)
    available = sorted(node for node, degree in indegree.items() if degree == 0)
    result = []
    while available:
        node = available.pop(0)
        result.append(node)
        for dependent in sorted(outgoing.get(node, set())):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                available.append(dependent)
        available.sort()
    if len(result) != len(nodes):
        raise ValueError("dependency cycle detected")
    return result
