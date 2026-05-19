def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    visited = {}
    
    def dfs(node):
        if node in visited:
            return visited[node]
        visited[node] = True
        result = any(dfs(dep) for dep in dependencies.get(node, []) if dep != node)
        visited[node] = result
        return result
    
    all_nodes = set(dependencies.keys()) | {dep for deps in dependencies.values() for dep in deps}
    return any(dfs(node) for node in all_nodes)
