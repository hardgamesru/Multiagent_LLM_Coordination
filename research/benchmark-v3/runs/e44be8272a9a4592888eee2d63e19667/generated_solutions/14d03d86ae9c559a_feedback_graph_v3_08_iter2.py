from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Инвертировать зависимости для нахождения изолированных узлов
    reverse_dependencies = defaultdict(list)
    for dep, deps in dependencies.items():
        for d in deps:
            reverse_dependencies[d].append(dep)
    
    # Найти узлы без зависимостей
    layers = []
    zero_in_degree_nodes = deque([node for node, deps in dependencies.items() if not deps])
    
    while zero_in_degree_nodes:
        current_layer = []
        
        # Собрать текущие свободные узлы
        for _ in range(len(zero_in_degree_nodes)):
            current_node = zero_in_degree_nodes.popleft()
            current_layer.append(current_node)
            
            # Проверить циклы: если найден узел без зависимостей среди зависимых
            if current_node in reverse_dependencies:
                raise ValueError("Cycle detected")
        
        # Добавить текущий слой
        layers.append(sorted(current_layer))
        
        # Обновить зависимости оставшихся узлов
        for node, deps in dependencies.items():
            if node not in current_layer:
                new_deps = [dep for dep in deps if dep not in current_layer]
                if not new_deps:
                    zero_in_degree_nodes.append(node)
    
    return layers
