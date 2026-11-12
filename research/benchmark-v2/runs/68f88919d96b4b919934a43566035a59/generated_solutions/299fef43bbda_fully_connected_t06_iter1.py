def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    graph = dependencies.copy()
    for deps in dependencies.values():
        for node in deps:
            if node not in graph:
                graph[node] = []

    visited: set[str] = set()
    rec_stack: set[str] = set()

    def dfs(v: str) -> bool:
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
