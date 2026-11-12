from collections import defaultdict, deque

def strongly_connected(graph):
    def reverse_graph(g):
        rev = defaultdict(list)
        for node in g:
            for neighbor in g[node]:
                rev[neighbor].append(node)
        return dict(rev)
    
    def dfs_visit(v, visited, stack):
        visited[v] = True
        for u in graph[v]:
            if not visited[u]:
                dfs_visit(u, visited, stack)
        stack.append(v)
    
    def rdfs_visit(v, visited, comp):
        visited[v] = True
        comp.add(v)
        for u in rev_graph[v]:
            if not visited[u]:
                rdfs_visit(u, visited, comp)
    
    n = len(graph)
    visited = [False]*n
    stack = []
    
    # First DFS pass to get topological order
    for v in range(n):
        if not visited[v]:
            dfs_visit(v, visited, stack)
    
    # Reverse graph
    rev_graph = reverse_graph(graph)
    
    # Second DFS pass to find SCCs
    visited = [False]*n
    sccs = []
    
    while stack:
        v = stack.pop()
        if not visited[v]:
            comp = set()
            rdfs_visit(v, visited, comp)
            sccs.append(sorted(comp))
    
    # Lexicographic sorting of components and their contents
    return sorted(sccs)
