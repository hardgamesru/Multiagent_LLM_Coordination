from collections import defaultdict, deque

def strongly_connected(graph):
    def dfs_visit(v, visited, stack):
        visited[v] = True
        for neighbor in graph.get(v, []):
            if not visited.get(neighbor, False):
                dfs_visit(neighbor, visited, stack)
        stack.append(v)
    
    def transpose_graph():
        transposed = defaultdict(list)
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                transposed[neighbor].append(node)
        return transposed
    
    n = len(graph)
    visited = {}
    stack = []
    
    # First DFS traversal to get reverse post-ordering
    for node in graph.keys():
        if not visited.get(node, False):
            dfs_visit(node, visited, stack)
    
    # Transpose graph for second DFS
    transposed = transpose_graph()
    
    # Second DFS with reversed order to find SCCs
    sccs = []
    while stack:
        v = stack.pop()
        if not visited.get(v, False):
            component = []
            dfs_visit(v, visited, component)
            sccs.append(sorted(component))
    
    # Lexicographic sorting of components and then entire result
    return sorted(sccs)
