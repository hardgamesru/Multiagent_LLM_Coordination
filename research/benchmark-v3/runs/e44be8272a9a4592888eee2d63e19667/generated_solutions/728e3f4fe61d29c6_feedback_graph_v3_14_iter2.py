from collections import deque

def strongly_connected(graph):
    def dfs(v, visited, stack):
        visited[v] = True
        for u in graph.get(v, []):
            if not visited[u]:
                dfs(u, visited, stack)
        stack.append(v)
    
    def rdfs(v, visited, components):
        visited[v] = True
        component.append(v)
        for u in rev_graph.get(v, []):
            if not visited[u]:
                rdfs(u, visited, component)
    
    # Создаем обратный граф
    rev_graph = {v:[] for v in graph}
    for u in graph:
        for v in graph[u]:
            rev_graph[v].append(u)
    
    n = len(graph)
    visited = [False]*n
    stack = []
    
    # Первый проход DFS для топологической сортировки
    for node in range(n):
        if not visited[node]:
            dfs(node, visited, stack)
    
    # Второй проход DFS для нахождения компонент
    visited = [False]*n
    components = []
    
    while stack:
        node = stack.pop()
        if not visited[node]:
            component = []
            rdfs(node, visited, component)
            # Сортируем компоненту лексикографически
            components.append(sorted(component))
    
    # Сортируем компоненты лексикографически
    return sorted(components)
