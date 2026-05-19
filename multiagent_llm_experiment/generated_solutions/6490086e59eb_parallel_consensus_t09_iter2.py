def resolve_build_order(dependencies):
    # Build full graph including tasks from both keys and values
    graph = {task: set() for task in dependencies.keys()}
    for dependent, deps in dependencies.items():
        for dep in deps:
            graph.setdefault(dep, set())
            graph[dep].add(dependent)
    
    # Compute initial indegree counts
    indegree = {node: len(deps) for node, deps in dependencies.items()}
    for node in graph:
        if node not in indegree:
            indegree[node] = 0
    
    # Collect starting points (nodes with no incoming edges)
    queue = deque(sorted([node for node, count in indegree.items() if count == 0]))
    
    result = []
    while queue:
        current = queue.popleft()
        result.append(current)
        
        # Decrease indegree for all neighbors and enqueue new start candidates
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.extend(sorted(node for node in graph if indegree[node] == 0))
    
    # Check for cycles
    if len(result) != len(graph):
        raise ValueError("Cyclic dependency detected")
    
    return result
