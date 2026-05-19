def resolve_build_order(dependencies):
    def dfs(node):
        visited.add(node)
        visiting.add(node)
        
        for neighbor in adj[node]:
            if neighbor in visiting:
                raise ValueError("Cycle detected")
            
            if neighbor not in visited:
                dfs(neighbor)
                
        visiting.remove(node)
        sorted_nodes.appendleft(node)
    
    # Build adjacency list representation
    adj = defaultdict(list)
    all_tasks = set()
    
    for task, deps in dependencies.items():
        all_tasks.add(task)
        for dep in deps:
            adj[dep].append(task)
            all_tasks.add(dep)
    
    # Sort tasks lexicographically
    sorted_tasks = sorted(all_tasks)
    
    # Initialize data structures
    visited = set()
    visiting = set()
    sorted_nodes = deque()
    
    # Perform topological sort using DFS
    for node in sorted_tasks:
        if node not in visited:
            dfs(node)
    
    return list(sorted_nodes)
