def detect_cycle(dependencies):
    def dfs(node, visiting):
        if node in visiting:
            return True  # Cycle detected
        if node in visited:
            return False  # Already processed this node
        
        visiting.add(node)
        for neighbor in dependencies.get(node, []):
            if dfs(neighbor, visiting):
                return True
            
        visiting.remove(node)  # Backtrack
        visited.add(node)
        return False
    
    all_nodes = set(dependencies.keys())
    for value_list in dependencies.values():
        all_nodes.update(value_list)
        
    visited = set()
    for node in all_nodes:
        if dfs(node, set()):
            return True
            
    return False
