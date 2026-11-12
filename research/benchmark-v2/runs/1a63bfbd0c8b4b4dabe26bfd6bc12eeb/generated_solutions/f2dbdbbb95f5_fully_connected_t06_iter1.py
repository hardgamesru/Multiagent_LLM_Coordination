def detect_cycle(dependencies: dict[str, list[str]]) -> bool:
    visited = set()
    stack = set()
    
    def dfs(task: str) -> bool:
        if task in stack:
            return True
        if task in visited:
            return False
        stack.add(task)
        for dep in dependencies.get(task, []):
            if dfs(dep):
                return True
        stack.remove(task)
        visited.add(task)
        return False
    
    for task in dependencies:
        if dfs(task):
            return True
    return False
