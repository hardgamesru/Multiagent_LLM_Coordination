def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    graph = {}
    for u, deps in dependencies.items():
        graph.setdefault(u, []).extend(deps)
        for v in deps:
            graph.setdefault(v, [])
    visited = set()
    rec_stack = set()

    def dfs(u):
        visited.add(u)
        rec_stack.add(u)
        for v in graph[u]:
            if v not in visited:
                if dfs(v):
                    return True
            elif v in rec_stack:
                return True
        rec_stack.remove(u)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False
