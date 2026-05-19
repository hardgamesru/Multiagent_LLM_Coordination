def resolve_build_order(dependencies):
    # Create adjacency list representation of dependencies
    adj = {task: deps[:] for task, deps in dependencies.items()}
    
    # Build reverse adjacency list to track incoming edges (dependencies)
    rev_adj = defaultdict(list)
    for task, deps in adj.items():
        for dep in deps:
            rev_adj[dep].append(task)
            
    # Initialize degrees dictionary with number of incoming edges per node
    degrees = {node: len(rev_adj.get(node, [])) for node in adj}
    
    # Collect all nodes from both keys and values
    all_nodes = set(adj.keys()) | set(dep for deps in adj.values() for dep in deps)
    
    # Add any additional nodes found in values but missing as keys
    for node in all_nodes - set(adj.keys()):
        adj[node] = []
        degrees[node] = 0
        
    # Queue for nodes ready to be processed (in-degree == 0), sorted lexicographically
    queue = deque(sorted([node for node, degree in degrees.items() if degree == 0]))
    
    result = []
    
    while queue:
        current_node = queue.popleft()
        result.append(current_node)
        
        # Decrease degrees of dependent nodes and add new zero-degree nodes to queue
        for neighbor in adj[current_node]:
            degrees[neighbor] -= 1
            if degrees[neighbor] == 0:
                queue.append(neighbor)
                
    # Check for cycles by comparing result length with total unique nodes
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
