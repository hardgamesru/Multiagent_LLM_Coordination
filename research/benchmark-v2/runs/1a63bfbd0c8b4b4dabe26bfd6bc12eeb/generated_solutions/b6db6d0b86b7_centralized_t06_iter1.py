def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    all_nodes = set(dependencies.keys()) | {dep for deps in dependencies.values() for dep in deps}
    state = {node: 0 for node in all_nodes}
    
    def dfs(node: str) -> bool:
        if state[node] == 1:
            return True
        if state[node] == 2:
            return False
        state[node] = 1
        for neighbor in dependencies.get(node, []):
            if dfs(neighbor):
                return True
        state[node] = 2
        return False
    
    for node in all_nodes:
        if state[node] != 2 and dfs(node):
            return True
    return False
