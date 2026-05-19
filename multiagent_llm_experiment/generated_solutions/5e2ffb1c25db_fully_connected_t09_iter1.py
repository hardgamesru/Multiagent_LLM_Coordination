def resolve_build_order(dependencies):
    nodes = set()
    reverse_dependencies = defaultdict(list)
    
    for node, deps in dependencies.items():
        nodes.add(node)
        nodes.update(deps)
        for dep in deps:
            reverse_dependencies[dep].append(node)
            
    indegree = {node: 0 for node in nodes}
    
    for _, deps in dependencies.items():
        for dep in deps:
            indegree[dep] += 1
            
    zero_indegree_nodes = [node for node in nodes if indegree[node] == 0]
    zero_indegree_nodes.sort()
    queue = deque(zero_indegree_nodes)
    
    result = []
    
    while queue:
        current_node = queue.popleft()
        result.append(current_node)
        
        for dependent in reverse_dependencies[current_node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                queue.append(dependent)
                
    if len(result) < len(nodes):
        raise ValueError("Circular dependency detected")
        
    return result
