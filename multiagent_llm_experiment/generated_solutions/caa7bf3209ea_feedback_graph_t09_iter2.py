def resolve_build_order(dependencies):
    # Build adjacency list and count incoming edges
    adj = defaultdict(list)
    indegree = {task: 0 for task in set(dependencies.keys())}
    
    # Populate adjacency list and calculate indegree counts
    for task, deps in dependencies.items():
        for dep in deps:
            adj[dep].append(task)
            indegree.setdefault(dep, 0)
            indegree[task] += 1
            
    # Add unreferenced nodes from values
    for deps in dependencies.values():
        for node in deps:
            indegree.setdefault(node, 0)
    
    # Queue for topological sorting (nodes with zero incoming edges)
    queue = deque(sorted([node for node, degree in indegree.items() if degree == 0]))
    result = []
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        for neighbor in sorted(adj[current]):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
                
    # Check for cycles by comparing length of result with total number of unique nodes
    if len(result) != len(indegree):
        raise ValueError("Cycle detected")
    
    return result
