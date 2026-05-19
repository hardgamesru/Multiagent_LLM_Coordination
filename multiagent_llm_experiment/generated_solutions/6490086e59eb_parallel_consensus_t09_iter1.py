def resolve_build_order(dependencies):
    # Build complete set of unique nodes including those appearing only in values
    all_nodes = set()
    for node, deps in dependencies.items():
        all_nodes.add(node)
        all_nodes.update(deps)
    
    # Initialize incoming edge count for each node
    in_degree = {node: 0 for node in all_nodes}
    
    # Calculate number of incoming edges per node 
    reverse_deps = defaultdict(list)  
    for node, deps in dependencies.items():
        for dep in deps:
            in_degree[node] += 1
            reverse_deps[dep].append(node)
            
    # Collect nodes with no incoming edges (ready to process first)
    queue = deque(sorted([node for node in all_nodes if in_degree[node] == 0]))
        
    # Resulting build order
    result = []
    
    while queue:
        current_node = queue.popleft()  # Get next node in lexicographic order
        result.append(current_node)
        
        # Decrease in-degree for dependent nodes and enqueue if now ready
        for dependent in sorted(reverse_deps[current_node]):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                
    # Check for cycles - all nodes should be processed without remaining edges
    if len(result) != len(all_nodes):
        raise ValueError("Graph contains a cycle")
        
    return result
