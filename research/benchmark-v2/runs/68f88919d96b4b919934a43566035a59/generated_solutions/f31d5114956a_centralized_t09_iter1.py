import heapq

def resolve_build_order(dependencies: dict[str, list[str]]) -> list[str]:
    all_nodes = set(dependencies.keys())
    for deps in dependencies.values():
        all_nodes.update(deps)

    graph = {node: [] for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}

    for node, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(node)
            in_degree[node] += 1

    heap = [node for node in all_nodes if in_degree[node] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, neighbor)

    if len(order) != len(all_nodes):
        raise ValueError("Graph contains a cycle")

    return order
