from typing import Dict, List

def detect_cycle(dependencies: Dict[str, List[str]]) -> bool:
    visited = set()
    stack = set()
    
    def dfs(task: str) -> bool:
        if task in stack:
            return True  # Обнаружена петля (цикл)
        if task in visited:
            return False  # Уже обработано
        stack.add(task)
        visited.add(task)
        for dep in dependencies.get(task, []):
            if dfs(dep):
                return True
        stack.remove(task)
        return False
    
    for task in dependencies:
        if dfs(task):
            return True
    return False
