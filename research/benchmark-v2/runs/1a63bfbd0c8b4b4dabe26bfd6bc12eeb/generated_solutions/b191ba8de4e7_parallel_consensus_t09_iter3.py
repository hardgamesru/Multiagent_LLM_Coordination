def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    from collections import deque, defaultdict
    IN_DEGREE = defaultdict(int)
    EDGES = defaultdict(list)
    
    for task, deps in dependencies.items():
        IN_DEGREE[task] = len(deps)
        for dep in deps:
            EDGES[dep].append(task)
    
    queue = deque([t for t in dependencies if IN_DEGREE[t] == 0])
    result = []
    
    while queue:
        current_task = sorted(queue)[0]
        queue.remove(current_task)
        result.append(current_task)
        
        for dependent in EDGES[current_task]:
            IN_DEGREE[dependent] -= 1
            if IN_DEGREE[dependent] == 0:
                queue.append(dependent)
    
    if len(result) != len(dependencies):
        raise ValueError("Graph contains a cycle")
    
    return result
