def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    """Returns a deterministic build order for tasks based on their dependencies.
       Each task depends on all tasks listed in its value. A task can be built 
       only after all its dependencies are built. If several tasks are ready at 
       the same time, they are chosen in lexicographical order. Raises ValueError 
       if there is a cycle in the dependency graph."""
    
    in_degree = {task: 0 for task in dependencies}
    graph = {task: set() for task in dependencies}
    
    for task, deps in dependencies.items():
        for dep in deps:
            in_degree[task] += 1
            graph[dep].add(task)
    
    queue = [task for task in in_degree if in_degree[task] == 0]
    result = []
    
    while queue:
        # Sort to ensure deterministic order when multiple tasks are ready
        current_tasks = sorted(queue)
        for task in current_tasks:
            queue.remove(task)
            result.append(task)
            
            for dependent in graph[task]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
    
    # Check for cycles
    if len(result) != len(in_degree):
        raise ValueError("Graph contains a cycle")
    
    return result
