import heapq
from collections import defaultdict

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
    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        current = heapq.heappop(heap)
        order.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                heapq.heappush(heap, neighbor)
    if len(order) != len(nodes):
        raise ValueError("Cycle detected")
    return order
