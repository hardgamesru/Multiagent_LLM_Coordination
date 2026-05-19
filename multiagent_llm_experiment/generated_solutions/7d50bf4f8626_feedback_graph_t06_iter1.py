def detect_cycle(dependencies):
    def dfs(node, visiting, visited):
        if node in visiting:
            return True  # Found a back-edge/cycle
        if node in visited:
            return False  # Already processed this node
        visiting.add(node)
        for neighbor in dependencies.get(node, []):
            if dfs(neighbor, visiting, visited):
                return True
        visiting.remove(node)  # Backtrack after exploring neighbors
        visited.add(node)
        return False

    visited = set()
    for node in dependencies.keys():
        if dfs(node, set(), visited):
            return True
    return False
