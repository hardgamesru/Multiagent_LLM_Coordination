def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    def dfs(task: str, visited: set[str], stack: set[str]) -> bool:
        if task in stack:
            return True
        if task in visited:
            return False
        visited.add(task)
        stack.add(task)
        for dep in dependencies.get(task, []):
            if dfs(dep, visited, stack):
                return True
        stack.remove(task)
        return False

    all_nodes = set(dependencies.keys())
    all_nodes.update(sum(dependencies.values(), []))
    for node in all_nodes:
        if node not in visited := set():
            if dfs(node, visited, set()):
                return True
    return False
