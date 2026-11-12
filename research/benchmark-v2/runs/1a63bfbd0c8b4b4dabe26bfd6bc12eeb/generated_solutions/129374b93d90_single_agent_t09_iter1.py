def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    from collections import deque, defaultdict
    in_degree = defaultdict(int)
    graph = defaultdict(list)
    
    for task, deps in dependencies.items():
        in_degree[task] = len(deps)
        for dep in deps:
            graph[dep].append(task)
    
    zero_indegree_tasks = deque([t for t in in_degree if in_degree[t] == 0])
    result = []
    
    while zero_indegree_tasks:
        task = zero_indegree_tasks.popleft()
        result.append(task)
        for neighbor in graph[task]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_indegree_tasks.append(neighbor)
    
    if len(result) != len(in_degree):
        raise ValueError("Graph contains a cycle")
    return result
