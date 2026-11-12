def strongly_connected(graph: dict[str, list[str]]) -> list[list[str]]:
    g = {u: list(vs) for u, vs in graph.items()}
    all_nodes = set(g.keys())
    for vs in g.values():
        all_nodes.update(vs)
    for u in all_nodes:
        g.setdefault(u, [])

    index = {}
    lowlink = {}
    index_counter = [0]
    stack = []
    on_stack = set()
    components = []

    def strongconnect(v):
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)

        for w in g[v]:
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
            components.append(sorted(comp))

    for v in sorted(all_nodes):
        if v not in index:
            strongconnect(v)

    return sorted(components)
