def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    in_degree = {task: 0 for task in dependencies}
    graph = {task: set() for task in dependencies}
    
    for task, deps in dependencies.items():
        for dep in deps:
            in_degree[task] += 1
            graph[dep].add(task)
    
    queue = sorted([task for task in in_degree if in_degree[task] == 0])
    result = []
    
    while queue:
        task = queue.pop(0)
        result.append(task)
        
        for dependent in graph[task]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    if len(result) != len(in_degree):
        raise ValueError("Cycle detected in dependencies")
    
    return result
