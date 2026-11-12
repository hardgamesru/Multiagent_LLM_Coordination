from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Инвертированный граф зависимостей для топологической сортировки
    inverted = defaultdict(list)
    for dep, deps in dependencies.items():
        for d in deps:
            inverted[d].append(dep)
    
    # Узлы без входящих зависимостей
    zero_in_degree = set(dependencies.keys()) - set(inverted.keys())
    
    result = []
    while zero_in_degree:
        current_layer = sorted(zero_in_degree)
        result.append(current_layer)
        
        next_nodes = []
        for node in zero_in_degree:
            # Удалить узлы, зависящие от текущего слоя
            for neighbor in dependencies[node]:
                inverted[neighbor].remove(node)
                # Добавляем узлы, ставшие свободными после удаления зависимых
                if not inverted[neighbor]:
                    next_nodes.append(neighbor)
        
        zero_in_degree = set(next_nodes)
    
    # Проверка циклов через оставшиеся зависимости
    if len(result) != len(dependencies):
        raise ValueError("Cycle detected")
    
    return result
