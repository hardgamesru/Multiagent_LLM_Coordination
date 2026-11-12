from collections import deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Узлы без входящих связей
    zero_in_degree = set(node for node, deps in dependencies.items() if not deps)
    
    # Все узлы
    nodes = set(dependencies.keys())
    
    layers = []
    
    while zero_in_degree:
        # Текущий слой - лексикографический порядок узлов без зависимостей
        current_layer = sorted(zero_in_degree)
        layers.append(current_layer)
        
        # Удалить текущие узлы из общего множества
        next_nodes = nodes - zero_in_degree
        
        # Найти узлы с новыми нулевыми степенями
        new_zero_in_degree = set()
        for node in next_nodes:
            deps = dependencies[node]
            # Убрать зависимости от уже обработанных узлов
            clean_deps = [dep for dep in deps if dep not in zero_in_degree]
            
            # Если все зависимости выполнены
            if not clean_deps:
                new_zero_in_degree.add(node)
                
        # Проверка цикла
        if len(new_zero_in_degree) != len(zero_in_degree):
            raise ValueError("Cycle detected")
        
        # Обновить множество узлов без входящих связей
        zero_in_degree = new_zero_in_degree
    
    return layers
