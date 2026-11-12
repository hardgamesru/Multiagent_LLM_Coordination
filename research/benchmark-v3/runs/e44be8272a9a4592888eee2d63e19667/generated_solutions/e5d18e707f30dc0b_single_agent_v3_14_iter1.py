def strongly_connected(graph):
    adj = {u: list(vs) for u, vs in graph.items()}
    for vs in graph.values():
        for v in vs:
            if v not in adj:
                adj[v] = []
    index = {}
    lowlink = {}
    stack = []
    onstack = set()
    sccs = []
    idx = 0
    def strongconnect(v):
        nonlocal idx
        index[v] = idx
        lowlink[v] = idx
        idx += 1
        stack.append(v)
        onstack.add(v)
        for w in adj[v]:
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in onstack:
                lowlink[v] = min(lowlink[v], index[w])
        if lowlink[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                onstack.remove(w)
                comp.append(w)
                if w == v:
                    break
            comp.sort()
            sccs.append(comp)
    for v in list(adj):
        if v not in index:
            strongconnect(v)
    sccs.sort()
    return sccs
