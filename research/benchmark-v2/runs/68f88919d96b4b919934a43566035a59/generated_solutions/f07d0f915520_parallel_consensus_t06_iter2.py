def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    graph = {}
    for node, deps in dependencies.items():
        graph.setdefault(node, []).extend(deps)
        for dep in deps:
            graph.setdefault(dep, [])
    visited = set()
    rec_stack = set()
    def dfs(v):
        visited.add(v)
        rec_stack.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(v)
        return False
    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False
