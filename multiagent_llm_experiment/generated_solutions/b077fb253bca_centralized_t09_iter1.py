def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    def dfs(node):
        visited.add(node)
        visiting.add(node)
        
        # Check dependencies of current node
        for dep in dependencies.get(node, []):
            if dep in visiting:
                raise ValueError("Cycle detected")
            
            if dep not in visited:
                dfs(dep)
                
        visiting.remove(node)
        result.insert(0, node)  # Prepend to maintain topological order
    
    # Collect all unique nodes (tasks), including those appearing only as dependencies
    all_nodes = set()
    for node, deps in dependencies.items():
        all_nodes.add(node)
        all_nodes.update(deps)
    
    sorted_nodes = sorted(all_nodes)  # Lexicographically sort nodes
    visited = set()                   # Track already processed nodes
    visiting = set()                  # Track current DFS path to detect cycles
    result = []
    
    for node in sorted_nodes:
        if node not in visited:
            dfs(node)
    
    return result
