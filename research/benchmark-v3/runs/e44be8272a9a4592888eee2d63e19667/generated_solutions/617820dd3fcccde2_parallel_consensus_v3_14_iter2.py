def strongly_connected(graph: dict[str, list[str]]) -> list[list[str]]:
    from collections import defaultdict

    adj = defaultdict(list)
    nodes = set(graph.keys())
    for u, nbrs in graph.items():
        adj[u].extend(nbrs)
        nodes.update(nbrs)
    for n in nodes:
        adj.setdefault(n, [])

    index = {}
    lowlink = {}
    stack = []
    on_stack = set()
    sccs = []
    idx = 0

    def strongconnect(v):
        nonlocal idx
        index[v] = idx
        lowlink[v] = idx
        idx += 1
        stack.append(v)
        on_stack.add(v)
        for w in adj[v]:
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])
        if lowlink[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            sccs.append(sorted(comp))

    for v in sorted(nodes):
        if v not in index:
            strongconnect(v)

    return sorted(sccs)
