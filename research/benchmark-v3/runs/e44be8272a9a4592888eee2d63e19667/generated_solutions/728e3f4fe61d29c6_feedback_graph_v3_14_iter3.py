from collections import defaultdict, deque

def strongly_connected(graph):
    def reverse_graph(g):
        rev = defaultdict(list)
        for u in g:
            for v in g[u]:
                rev[v].append(u)
        return dict(rev)
    
    def dfs_visit(v, visited, stack):
        visited.add(v)
        for neighbor in graph.get(v, []):
            if neighbor not in visited:
                dfs_visit(neighbor, visited, stack)
        stack.append(v)
    
    def dfs_reverse(g, start, visited, comp):
        visited.add(start)
        comp.add(start)
        for neighbor in g[start]:
            if neighbor not in visited:
                dfs_reverse(g, neighbor, visited, comp)
    
    # Step 1: Find topological order using Kahn's algorithm with DFS
    reversed_order = []
    visited = set()
    for node in graph:
        if node not in visited:
            stack = deque()
            dfs_visit(node, visited, stack)
            while stack:
                reversed_order.append(stack.pop())
    
    # Step 2: Create reverse graph
    rev_graph = reverse_graph(graph)
    
    # Step 3: Find SCCs using Kosaraju's algorithm
    sccs = []
    visited = set()
    for node in reversed_order:
        if node not in visited:
            comp = set()
            dfs_reverse(rev_graph, node, visited, comp)
            sccs.append(sorted(comp))
    
    # Sort components lexicographically by their contents
    sccs.sort()
    return sccs
