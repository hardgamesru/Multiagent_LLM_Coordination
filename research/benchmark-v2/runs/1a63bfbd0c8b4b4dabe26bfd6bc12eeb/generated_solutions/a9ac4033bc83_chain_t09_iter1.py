def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    from collections import deque, defaultdict
    graph = defaultdict(list)
    in_degree = {}
    
    for task, deps in dependencies.items():
        in_degree[task] = 0
        for dep in deps:
            graph[dep].append(task)
            in_degree[task] += 1
    
    queue = deque([t for t in in_degree if in_degree[t] == 0])
    order = []
    
    while queue:
        task = queue.popleft()
        order.append(task)
        
        for neighbor in graph[task]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != len(in_degree):
        raise ValueError("Cycle detected")
    
    return order
