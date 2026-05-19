def resolve_build_order(dependencies):
    # Collect all unique tasks including those appearing only in values
    all_tasks = set()
    for k, v in dependencies.items():
        all_tasks.add(k)
        all_tasks.update(v)
    
    # Build adjacency list representation of the graph
    adj_list = {task: [] for task in all_tasks}
    indegree = {task: 0 for task in all_tasks}  # Track incoming edges
    
    for task, deps in dependencies.items():
        for dep in deps:
            adj_list[dep].append(task)  # Add edge from dependency to dependent task
            indegree[task] += 1         # Increment count of incoming edges for dependent task
    
    # Queue for tasks with no incoming edges (ready to process)
    queue = deque(sorted([t for t in all_tasks if indegree[t] == 0]))
    
    result = []
    
    while queue:
        node = queue.popleft()          # Get next task in lexicographic order
        result.append(node)             # Add to result
        
        # Decrement indegree for all tasks depending on current node
        for neighbor in adj_list[node]:
            indegree[neighbor] -= 1
            
            # If a task has no more incoming edges, add it to the queue
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycles - if we didn't visit all tasks, there's a cycle
    if len(result) != len(all_tasks):
        raise ValueError("Graph contains a cycle")
    
    return result
