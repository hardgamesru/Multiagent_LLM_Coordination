from collections import defaultdict, deque

def strongly_connected(graph):
    def dfs_visit(v, visited, stack):
        visited[v] = True
        for neighbor in graph.get(v, []):
            if not visited[neighbor]:
                dfs_visit(neighbor, visited, stack)
        stack.append(v)
    
    def rdfs_visit(v, rev_graph, comp):
        comp.add(v)
        visited_r[v] = True
        for neighbor in rev_graph.get(v, []):
            if not visited_r[neighbor]:
                rdfs_visit(neighbor, rev_graph, comp)
    
    n = len(graph)
    visited = [False]*n
    stack = []
    
    # First DFS pass to get reverse post-ordering
    for node in range(n):
        if not visited[node]:
            dfs_visit(node, visited, stack)
    
    # Create reversed graph
    rev_graph = defaultdict(list)
    for u in graph:
        for v in graph[u]:
            rev_graph[v].append(u)
    
    visited_r = [False]*n
    components = []
    
    # Second DFS pass to find SCCs using reverse post-ordering
    while stack:
        node = stack.pop()
        if not visited_r[node]:
            comp_set = set()
            rdfs_visit(node, rev_graph, comp_set)
            components.append(sorted(comp_set))
    
    return sorted(components)
