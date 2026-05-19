def resolve_build_order(dependencies):
    def dfs(node):
        visited.add(node)
        visiting.add(node)
        
        for neighbor in dependencies.get(node, []):
            if neighbor in visiting:
                raise ValueError("Cycle detected")
            
            if neighbor not in visited:
                dfs(neighbor)
                
        visiting.remove(node)
        result.appendleft(node)
    
    from collections import deque
    result = deque()
    visited = set()
    visiting = set()
    
    # Добавляем все узловые точки из зависимостей
    all_nodes = set(dependencies.keys())
    for deps in dependencies.values():
        all_nodes.update(deps)
    
    sorted_nodes = sorted(all_nodes)  # Лексикографическое упорядочивание узлов
    
    for node in sorted_nodes:
        if node not in visited:
            dfs(node)
    
    return list(result)
