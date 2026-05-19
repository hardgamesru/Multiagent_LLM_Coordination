def detect_cycle(dependencies):
    def dfs(node, visiting):
        if node in visited:
            return False
        if node in visiting:
            return True
        visiting.add(node)
        for neighbor in dependencies.get(node, []):
            if dfs(neighbor, visiting):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    all_nodes = set(dependencies.keys())
    for deps in dependencies.values():
        all_nodes.update(deps)
    
    visited = set()
    for node in all_nodes:
        if dfs(node, set()):
            return True
    return False
