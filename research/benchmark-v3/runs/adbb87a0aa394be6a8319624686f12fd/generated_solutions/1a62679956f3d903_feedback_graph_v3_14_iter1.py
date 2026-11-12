from typing import Dict, List
from collections import deque

def strongly_connected(graph: Dict[str, List[str]]) -> List[List[str]]:
    def dfs(v):
        visited.add(v)
        for u in graph[v]:
            if u not in visited:
                dfs(u)
        stack.append(v)
    
    def rdfs(v):
        visited.add(v)
        scc.append(v)
        for u in rev_graph[v]:
            if u not in visited:
                rdfs(u)
    
    n = len(graph)
    visited = set()
    stack = []
    # Build reverse graph for Kosaraju's algorithm
    rev_graph = {v:[] for v in graph}
    for v in graph:
        for u in graph[v]:
            rev_graph[u].append(v)
    
    sccs = []
    while stack:
        v = stack.pop()
        if v not in visited:
            scc = []
            rdfs(v)
            # Lexicographic sorting within SCC
            scc.sort()
            sccs.append(scc)
    
    # Outer list sorted lexicographically
    return sorted(sccs)
