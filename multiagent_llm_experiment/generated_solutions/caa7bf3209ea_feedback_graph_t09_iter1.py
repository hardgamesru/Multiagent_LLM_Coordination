def resolve_build_order(dependencies):
    # Step 1: Build complete adjacency list including unreferenced nodes
    adj = defaultdict(list)
    indegree = {task: 0 for task in dependencies.keys()}
    
    # Collect all unique tasks from both keys and values
    all_tasks = set()
    for task, deps in dependencies.items():
        all_tasks.add(task)
        for dep in deps:
            all_tasks.add(dep)
    
    # Initialize indegree count for all tasks
    for task in all_tasks:
        indegree.setdefault(task, 0)
    
    # Create full dependency structure
    for task, deps in dependencies.items():
        for dep in deps:
            adj[dep].append(task)  # Reverse direction since we want topological sort
            indegree[task] += 1     # Increment indegree for this task
    
    # Step 2: Topological Sort using Kahn's algorithm
    queue = deque(sorted([task for task in indegree if indegree[task] == 0]))
    result = []
    
    while queue:
        current_task = queue.popleft()
        result.append(current_task)
        
        for neighbor in sorted(adj[current_task]):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycles by comparing length of result with total number of tasks
    if len(result) != len(all_tasks):
        raise ValueError("Cycle detected in dependency graph")
    
    return result
