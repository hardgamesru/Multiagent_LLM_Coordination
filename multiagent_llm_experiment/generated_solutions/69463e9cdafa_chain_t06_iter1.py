def detect_cycle(dependencies):
    def dfs(node, visiting, visited):
        if node in visiting:
            return True  # Found a back edge, hence a cycle
        if node in visited:
            return False  # Already processed this node
        
        visiting.add(node)
        for neighbor in dependencies.get(node, []):
            if dfs(neighbor, visiting, visited):
                return True
        visiting.remove(node)
        visited.add(node)
        return False
    
    all_nodes = set(dependencies.keys())
    for value_list in dependencies.values():
        all_nodes.update(value_list)
    
    visited = set()
    for node in all_nodes:
        if dfs(node, set(), visited):
            return True
    return False
