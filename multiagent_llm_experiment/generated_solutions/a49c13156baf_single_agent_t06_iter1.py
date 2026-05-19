def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    nodes = set(dependencies)
    for deps in dependencies.values():
        nodes.update(deps)
    visiting = set()
    visited = set()

    def visit(node):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dep in dependencies.get(node, []):
            if visit(dep):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in nodes)
