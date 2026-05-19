def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    # Collect all unique nodes including those appearing only in dependency lists
    nodes = set()
    reverse_deps = defaultdict(list)
    
    for task, deps in dependencies.items():
        nodes.add(task)
        for dep in deps:
            nodes.add(dep)
            reverse_deps[dep].append(task)
            
    # Initialize incoming edge count for each node
    in_degree = {node: 0 for node in nodes}
    for _, deps in dependencies.items():
        for dep in deps:
            in_degree[dep] += 1
        
    # Queue for processing nodes with zero incoming edges
    queue = deque(sorted([node for node in nodes if in_degree[node] == 0]))
    result = []
    
    while queue:
        current_node = queue.popleft()
        result.append(current_node)
        
        # Decrease in-degree for dependent nodes
        for next_node in reverse_deps[current_node]:
            in_degree[next_node] -= 1
            if in_degree[next_node] == 0:
                queue.append(next_node)
                
    # Check for cycles by comparing number of processed nodes vs total nodes
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
        
    return result
