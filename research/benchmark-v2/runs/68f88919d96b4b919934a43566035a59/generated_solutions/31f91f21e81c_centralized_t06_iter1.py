def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    if not dependencies:
        return False

    all_nodes = set(dependencies.keys())
    for deps in dependencies.values():
        all_nodes.update(deps)

    state = {node: 0 for node in all_nodes}

    def dfs(node: str) -> bool:
        state[node] = 1
        for neighbor in dependencies.get(node, []):
            if state[neighbor] == 0:
                if dfs(neighbor):
                    return True
            elif state[neighbor] == 1:
                return True
        state[node] = 2
        return False

    for node in all_nodes:
        if state[node] == 0:
            if dfs(node):
                return True
    return False
