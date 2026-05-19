def detect_cycle(dependencies):
    def dfs(node, visiting, visited):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for neighbor in dependencies.get(node, []):
            if dfs(neighbor, visiting, visited):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    all_nodes = set(dependencies.keys())
    for deps in dependencies.values():
        all_nodes.update(deps)
    
    visited = set()
    for node in all_nodes:
        if dfs(node, set(), visited):
            return True
    return False
