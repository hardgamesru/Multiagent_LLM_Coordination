from typing import Dict, List
from collections import deque, defaultdict

def strongly_connected(graph: Dict[str, List[str]]) -> List[List[str]]:
    def dfs(v):
        visited.add(v)
        for u in graph[v]:
            if u not in visited:
                dfs(u)
    
    def reverse_dfs(v):
        stack.append(v)
        visited.add(v)
        for u in rev_graph[v]:
            if u not in visited:
                reverse_dfs(u)
    
    # Create reversed graph
    rev_graph = defaultdict(list)
    for v in graph:
        for u in graph[v]:
            rev_graph[u].append(v)
    
    # Find SCC using Kosaraju's algorithm
    visited = set()
    stack = []
    sccs = []
    
    for node in graph:
        if node not in visited:
            reverse_dfs(node)
    
    seen = set()
    while stack:
        v = stack.pop()
        if v not in seen:
            comp = []
            dfs(v)
            comp.sort()
            sccs.append(comp)
            seen.update(comp)
    
    return sorted(sccs)
