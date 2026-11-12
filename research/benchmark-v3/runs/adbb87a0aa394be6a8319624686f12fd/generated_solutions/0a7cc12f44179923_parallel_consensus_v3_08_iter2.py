from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Инвертированный граф зависимостей
    reverse_graph = defaultdict(list)
    in_degree = {}
    
    for node, deps in dependencies.items():
        in_degree[node] = len(deps)
        for dep in deps:
            reverse_graph[dep].append(node)
    
    # Очередь свободных узлов
    queue = deque([node for node, degree in in_degree.items() if degree == 0])
    
    layers = []
    while queue:
        current_layer = []
        
        # Собираем текущий слой
        for _ in range(len(queue)):
            node = queue.popleft()
            current_layer.append(node)
            
            # Обрабатываем зависимости текущего узла
            for neighbor in reverse_graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Добавляем текущий слой в результат
        layers.append(sorted(current_layer))
    
    # Проверка циклов зависимостей
    if len(layers) != len(in_degree):
        raise ValueError("Cycle detected in dependencies")
    
    return layers
