def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    visited = set()
    def dfs(task: str, stack: set) -> bool:
        if task in stack: return True
        if task in visited: return False
        visited.add(task)
        stack.add(task)
        for dep in dependencies.get(task, []):
            if dfs(dep, stack): return True
        stack.remove(task)
        return False
    for task in dependencies:
        if dfs(task, set()): return True
    return False
