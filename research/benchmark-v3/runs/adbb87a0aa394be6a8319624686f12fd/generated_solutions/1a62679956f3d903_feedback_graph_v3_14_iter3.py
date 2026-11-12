from collections import deque

def strongly_connected(graph):
    def dfs(v, visited, stack):
        visited[v] = True
        for neighbor in graph.get(v, []):
            if not visited[neighbor]:
                dfs(neighbor, visited, stack)
        stack.appendleft(v)
    
    # First pass: topological sorting using Kahn's algorithm
    reversed_graph = {v: set() for v in graph}
    for u, neighbors in graph.items():
        for v in neighbors:
            reversed_graph[v].add(u)
    
    in_degree = {node: len(reversed_graph[node]) for node in reversed_graph}
    queue = deque([node for node in graph if in_degree[node] == 0])
    topo_order = []
    
    while queue:
        current = queue.popleft()
        topo_order.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Second pass: finding SCCs using Kosaraju's algorithm
    visited = {node: False for node in graph}
    sccs = []
    stack = deque()
    
    for node in reversed(topo_order):
        if not visited[node]:
            component = []
            dfs(node, visited, stack)
            while stack:
                component.append(stack.popleft())
            sccs.append(component)
    
    return sorted([sorted(comp) for comp in sccs])
