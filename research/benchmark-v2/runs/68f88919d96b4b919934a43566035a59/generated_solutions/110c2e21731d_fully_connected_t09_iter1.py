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
    for n in nodes:
        indegree.setdefault(n, 0)
    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(heap, v)
    if len(order) != len(nodes):
        raise ValueError("Cycle detected")
    return order
