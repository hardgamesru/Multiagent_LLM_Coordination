def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    from collections import deque, defaultdict
    in_degree = defaultdict(int)
    graph = defaultdict(list)
    nodes = set()
    
    for task, deps in dependencies.items():
        nodes.add(task)
        for dep in deps:
            nodes.add(dep)
            in_degree[task] += 1
            graph[dep].append(task)
    
    zero_indegree = deque([n for n in nodes if in_degree[n] == 0])
    order = []
    
    while zero_indegree:
        node = zero_indegree.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_indegree.append(neighbor)
    
    if len(order) != len(nodes):
        raise ValueError("Cycle detected")
    
    return sorted(order)  # Sort to ensure deterministic behavior
