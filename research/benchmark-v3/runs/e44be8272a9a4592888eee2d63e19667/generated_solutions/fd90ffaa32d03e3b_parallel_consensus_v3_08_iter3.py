from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Инвертированная карта зависимостей: узел → узлы, зависящие от него
    reverse_dependencies = defaultdict(list)
    for dep, deps in dependencies.items():
        for d in deps:
            reverse_dependencies[d].append(dep)
    
    # Узлы без зависимостей
    zero_in_degree = set(dependencies.keys()) - set(reverse_dependencies.keys())
    
    result = []
    while zero_in_degree:
        current_layer = sorted(zero_in_degree)
        result.append(current_layer)
        
        # Обновляем зависимости оставшихся узлов
        next_zero_in_degree = set()
        for node in current_layer:
            for dependent_node in dependencies[node]:
                reverse_dependencies[dependent_node].remove(node)
                if not reverse_dependencies[dependent_node]:
                    next_zero_in_degree.add(dependent_node)
        
        zero_in_degree = next_zero_in_degree
    
    # Проверка циклов через оставшиеся обратные зависимости
    if any(reverse_dependencies.values()):
        raise ValueError("Cycle detected")
    
    return result
