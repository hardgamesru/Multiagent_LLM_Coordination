def build_layers(dependencies: dict[str, list[str]]) -> list[list[str]]:
    from collections import defaultdict, deque

    all_nodes = set(dependencies.keys())
    for deps in dependencies.values():
        all_nodes.update(deps)

    graph = defaultdict(list)
    indegree = {node: 0 for node in all_nodes}

    for node, deps in dependencies.items():
        for dep in set(deps):
            graph[dep].append(node)
            indegree[node] += 1

    zero_indegree = [n for n, d in indegree.items() if d == 0]
    zero_indegree.sort()
    queue = deque(zero_indegree)

    result: list[list[str]] = []
    processed_count = 0

    while queue:
        layer_size = len(queue)
        current_layer = []
        for _ in range(layer_size):
            node = queue.popleft()
            current_layer.append(node)
            processed_count += 1
            for dependent in graph[node]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)
        current_layer.sort()
        result.append(current_layer)

    if processed_count != len(all_nodes):
        raise ValueError("Cycle detected in dependencies")

    return result
