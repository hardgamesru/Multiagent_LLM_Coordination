from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Инвертировать зависимости для нахождения свободных узлов
    reverse_dependencies = defaultdict(list)
    for node, deps in dependencies.items():
        for dep in deps:
            reverse_dependencies[dep].append(node)
    
    # Найти узлы без зависимостей
    free_nodes = set(dependencies.keys()) - set(reverse_dependencies.keys())
    
    result = []
    while free_nodes:
        # Сортировка и добавление текущего слоя
        current_layer = sorted(free_nodes)
        result.append(current_layer)
        
        # Удалить текущие узлы из всех зависимостей
        for node in current_layer:
            for dep_node in dependencies.keys():
                if node in dependencies[dep_node]:
                    dependencies[dep_node].remove(node)
        
        # Обновить свободные узлы
        free_nodes = set(dependencies.keys()) - set(reverse_dependencies.keys())
    
    # Проверка циклов зависимостей
    if len(result) != len(dependencies):
        raise ValueError("Cycle detected in dependencies")
    
    return result
