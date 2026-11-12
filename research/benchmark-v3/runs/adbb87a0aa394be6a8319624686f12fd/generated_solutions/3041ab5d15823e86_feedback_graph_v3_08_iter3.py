from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Инвертировать зависимости для проверки циклов
    reverse_dependencies = defaultdict(list)
    for dep, deps in dependencies.items():
        for d in deps:
            reverse_dependencies[d].append(dep)
    
    # Найти узлы без входов
    zero_in_degree = set(dependencies.keys())
    for deps in dependencies.values():
        zero_in_degree -= set(deps)
    
    # Проверить наличие цикла
    if len(zero_in_degree) != len(dependencies):
        raise ValueError("Cycle detected")
    
    # Сортировка узлов для стабильного результата
    sorted_nodes = sorted(zero_in_degree)
    
    # Создать слои
    layers = []
    while sorted_nodes:
        current_layer = sorted_nodes[:]
        
        # Обнулить зависимости для текущего слоя
        for node in current_layer:
            del dependencies[node]
        
        # Удалить использованные зависимости
        for node, deps in dependencies.copy().items():
            dependencies[node] = [d for d in deps if d not in current_layer]
        
        # Добавить текущий слой
        layers.append(current_layer)
    
    return layers
