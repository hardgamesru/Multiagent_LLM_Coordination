from typing import Dict, List
from collections import deque, defaultdict

def strongly_connected(graph: Dict[str, List[str]]) -> List[List[str]]:
    def dfs(v):
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                dfs(neighbor)
    
    def reverse_graph():
        rev = defaultdict(list)
        for node in graph:
            for neighbor in graph[node]:
                rev[neighbor].append(node)
        return dict(rev)
    
    # Find first pass DFS order
    visited = set()
    stack = []
    for node in graph:
        if node not in visited:
            dfs(node)
            stack.append(node)
    
    # Reverse graph and second DFS to get SCCs
    rev_graph = reverse_graph()
    sccs = []
    while stack:
        v = stack.pop()
        if v not in visited:
            comp = []
            dfs(v, rev_graph, comp)
            sccs.append(sorted(comp))
    
    return sorted(sccs)
