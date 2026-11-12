def strongly_connected(graph: dict[str, list[str]]) -> list[list[str]]:
    all_nodes = set(graph.keys())
    for nbrs in graph.values():
        all_nodes.update(nbrs)
    index = 0
    indices = {}
    lowlink = {}
    stack = []
    on_stack = set()
    components = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph.get(v, []):
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
            components.append(sorted(comp))

    for v in sorted(all_nodes):
        if v not in indices:
            strongconnect(v)
    return sorted(components)
