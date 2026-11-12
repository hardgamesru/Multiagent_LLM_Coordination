def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    graph = {}
    for u, deps in dependencies.items():
        graph.setdefault(u, []).extend(deps)
        for v in deps:
            graph.setdefault(v, [])
    visited = set()
    rec_stack = set()
    def dfs(node):
        if node in rec_stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
        rec_stack.remove(node)
        return False
    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False
