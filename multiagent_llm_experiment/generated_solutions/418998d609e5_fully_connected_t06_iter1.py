def detect_cycle(dependencies):
    def dfs(node, visiting):
        if node in visited:
            return False
        if node in visiting:
            return True  # Cycle detected
        
        visiting.add(node)
        deps = dependencies.get(node, [])
        for dep in deps:
            if dfs(dep, visiting):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    visited = set()
    all_nodes = set(dependencies.keys())
    
    # Add nodes appearing only in values
    for v in dependencies.values():
        all_nodes.update(v)
    
    for node in all_nodes:
        if dfs(node, set()):
            return True
    return False
