def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    visited = {}
    
    def dfs(node):
        if node in visited:
            return visited[node]
        
        # Mark as visiting (gray)
        visited[node] = True
        
        for neighbor in dependencies.get(node, []):
            if dfs(neighbor) or visited.get(neighbor, None):
                return True  # Cycle detected
            
        # Mark as fully explored (black)
        visited[node] = False
        return False
    
    all_nodes = set(dependencies.keys())
    for value_list in dependencies.values():
        all_nodes.update(value_list)
    
    for node in all_nodes:
        if dfs(node):
            return True
            
    return False
