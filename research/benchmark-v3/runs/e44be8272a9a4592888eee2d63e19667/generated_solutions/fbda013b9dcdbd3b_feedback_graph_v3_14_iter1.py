def strongly_connected(graph: dict[str, list[str]]) -> list[list[str]]:
    adj = {u: list(vs) for u, vs in graph.items()}
    nodes = set(adj.keys())
    for vs in adj.values():
        nodes.update(vs)
    for v in nodes:
        adj.setdefault(v, [])

    index = 0
    indices = {}
    lowlink = {}
    stack = []
    on_stack = set()
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in adj[v]:
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            comp.sort()
            sccs.append(comp)

    for v in sorted(nodes):
        if v not in indices:
            strongconnect(v)

    sccs.sort()
    return sccs
