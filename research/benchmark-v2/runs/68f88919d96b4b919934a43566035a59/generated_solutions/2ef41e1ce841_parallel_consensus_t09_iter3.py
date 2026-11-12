from collections import defaultdict, deque

def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
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
    queue = deque(sorted([n for n in nodes if indegree[n] == 0]))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in sorted(graph[node]):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != len(nodes):
        raise ValueError("Cycle detected")
    return order
