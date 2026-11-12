from typing import Dict, List
from collections import deque

def strongly_connected(graph: Dict[str, List[str]]) -> List[List[str]]:
    def dfs(v):
        visited.add(v)
        for u in graph[v]:
            if u not in visited:
                dfs(u)
    
    def rdfs(v):
        stack.append(v)
        visited_r.add(v)
        for u in rev_graph[v]:
            if u not in visited_r:
                rdfs(u)
    
    # Create reverse graph for Kosaraju's algorithm
    rev_graph = {v:[] for v in graph}
    for src in graph:
        for dest in graph[src]:
            rev_graph[dest].append(src)
    
    n = len(graph)
    visited = set()
    visited_r = set()
    stack = []
    
    # First pass: get order of vertices
    for node in graph:
        if node not in visited:
            dfs(node)
    
    # Second pass: find SCCs using reversed graph
    sccs = []
    while stack:
        v = stack.pop()
        if v not in visited_r:
            comp = []
            rdfs(v)
            comp.sort()  
            sccs.append(comp)
    
    return sorted(sccs)
