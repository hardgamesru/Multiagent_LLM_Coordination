def resolve_build_order(dependencies):
    from collections import defaultdict, deque

    graph = defaultdict(list)
    indegree = defaultdict(int)
    nodes = set(dependencies.keys())
    for task, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task)
            indegree[task] += 1
            nodes.add(dep)

    for node in nodes:
        indegree.setdefault(node, 0)

    available = sorted([n for n in nodes if indegree[n] == 0])
    queue = deque(available)
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in sorted(graph[current]):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(nodes):
        raise ValueError("Cycle detected")
    return order
