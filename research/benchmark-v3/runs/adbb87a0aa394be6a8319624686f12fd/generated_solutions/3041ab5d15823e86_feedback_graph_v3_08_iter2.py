from collections import deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Подсчёт входных степеней всех узлов
    in_degree = {node: len(deps) for node, deps in dependencies.items()}
    # Узлы без входящих зависимостей
    zero_indegree_nodes = [node for node in dependencies if in_degree[node] == 0]
    
    layers = []
    while zero_indegree_nodes:
        # Слой — узлы без зависимостей, отсортированные лексикографически
        layer = sorted(zero_indegree_nodes)
        layers.append(layer)
        
        # Обновляем зависимости оставшихся узлов
        next_layer = []
        for node in zero_indegree_nodes:
            for dep in dependencies.get(node, []):
                in_degree[dep] -= 1
                # Добавляем узлы, ставшие свободными от зависимостей
                if in_degree[dep] == 0:
                    next_layer.append(dep)
        
        # Проверка цикла зависимостей
        if len(next_layer) != len(zero_indegree_nodes):
            raise ValueError("Cycle detected in dependencies")
            
        zero_indegree_nodes = next_layer
    
    return layers
