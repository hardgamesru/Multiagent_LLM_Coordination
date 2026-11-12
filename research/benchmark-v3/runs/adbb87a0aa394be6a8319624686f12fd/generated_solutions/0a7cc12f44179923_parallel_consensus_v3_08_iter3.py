from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Граф зависимостей и вход-выход степени каждого узла
    graph = defaultdict(list)
    in_degree = {node: len(deps) for node, deps in dependencies.items()}
    out_degree = {node: len(deps) for node, deps in dependencies.items()}
    
    # Очередь свободных узлов
    queue = deque([node for node, deg in in_degree.items() if deg == 0])
    
    # Итоговый результат слоёв
    layers = []
    
    while queue:
        current_layer = []
        
        # Собираем текущий слой
        for _ in range(len(queue)):
            node = queue.popleft()
            current_layer.append(node)
            
            # Обновляем зависимости других узлов
            for neighbor in graph[node]:
                out_degree[neighbor] -= 1
                if out_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Добавляем текущий слой в результат
        layers.append(sorted(current_layer))
    
    # Проверка наличия циклов через степень выхода
    for node, degree in out_degree.items():
        if degree != 0:
            raise ValueError("Cycle detected in dependencies")
    
    return layers
