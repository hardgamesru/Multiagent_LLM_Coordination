from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Инверсия зависимостей: узел зависит от всех своих зависимых узлов
    inverted = defaultdict(list)
    for dep, deps in dependencies.items():
        for d in deps:
            inverted[d].append(dep)
    
    # Узлы без зависимостей и их счетчики зависимостей
    zero_in_degree = set(dependencies.keys())
    for deps in dependencies.values():
        zero_in_degree -= set(deps)
    
    result = []
    while zero_in_degree:
        current_layer = sorted(zero_in_degree)
        
        # Проверка циклов через оставшиеся зависимости
        next_nodes = set()
        for node in zero_in_degree:
            for dep in dependencies[node]:
                if dep in zero_in_degree:
                    next_nodes.add(dep)
        
        # Обнаружен цикл
        if len(next_nodes) != len(zero_in_degree):
            raise ValueError("Cycle detected")
        
        # Добавляем текущий слой и обновляем счетчики зависимостей
        result.append(current_layer)
        zero_in_degree = next_nodes
    
    return result
