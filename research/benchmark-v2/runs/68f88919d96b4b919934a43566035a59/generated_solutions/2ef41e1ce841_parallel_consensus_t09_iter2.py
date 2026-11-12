from collections import defaultdict, deque

def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    graph = defaultdict(list)
    indegree = defaultdict(int)
    all_nodes = set(dependencies.keys())
    for task, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task)
            indegree[task] += 1
            all_nodes.add(dep)
    for node in all_nodes:
        indegree.setdefault(node, 0)
    queue = deque(sorted([n for n in all_nodes if indegree[n] == 0]))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in sorted(graph[node]):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
        queue = deque(sorted(queue))
    if len(order) != len(all_nodes):
        raise ValueError("Cycle detected")
    return order
