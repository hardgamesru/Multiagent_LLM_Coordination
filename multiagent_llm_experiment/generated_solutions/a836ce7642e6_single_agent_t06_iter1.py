def detect_cycle(dependencies: Dict[str, List[str]]) -> bool:
    visited = set()
    recursion_stack = set()
    
    def dfs(node):
        if node in recursion_stack:
            return True  # Cycle detected
        
        if node in visited:
            return False
            
        visited.add(node)
        recursion_stack.add(node)
        
        for neighbor in dependencies.get(node, []):
            if dfs(neighbor):
                return True
                
        recursion_stack.remove(node)
        return False
    
    all_nodes = set(dependencies.keys())
    for value_list in dependencies.values():
        all_nodes.update(value_list)
    
    for node in all_nodes:
        if dfs(node):
            return True
    
    return False
