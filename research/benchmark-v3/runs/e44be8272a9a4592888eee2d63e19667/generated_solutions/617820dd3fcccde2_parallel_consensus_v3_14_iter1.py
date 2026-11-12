def strongly_connected(graph: dict[str, list[str]]) -> list[list[str]]:
    from collections import defaultdict

    # Собираем все узлы, включая те, что есть только в значениях
    nodes = set(graph.keys())
    for nbrs in graph.values():
        nodes.update(nbrs)

    # Строим полный граф с копиями списков
    g = {v: list(graph.get(v, [])) for v in nodes}

    index = {}
    lowlink = {}
    index_counter = [0]
    stack = []
    on_stack = set()
    sccs = []

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
            component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == v:
                    break
            sccs.append(sorted(component))

    for v in sorted(nodes):
        if v not in index:
            strongconnect(v)

    return sorted(sccs)
