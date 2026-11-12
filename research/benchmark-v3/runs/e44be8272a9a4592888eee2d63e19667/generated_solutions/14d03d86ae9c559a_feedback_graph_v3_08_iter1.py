from collections import deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # Подсчёт входных степеней всех узлов
    in_degree = {node: len(deps) for node, deps in dependencies.items()}
    # Узлы без входных зависимостей
    zero_indegree_nodes = [node for node in dependencies if in_degree[node] == 0]
    
    layers = []
    while zero_indegree_nodes:
        # Слой - узлы без зависимостей, отсортированные лексикографически
        layer = sorted(zero_indegree_nodes)
        layers.append(layer)
        
        # Обновляем зависимости оставшихся узлов
        next_zero_indegree = []
        for node in zero_indegree_nodes:
            for dep in dependencies.get(node, []):
                in_degree[dep] -= 1
                # Добавляем узлы, ставшие свободными после снятия зависимостей
                if in_degree[dep] == 0:
                    next_zero_indegree.append(dep)
        
        # Проверка циклов зависимостей
        if len(next_zero_indegree) != len(zero_indegree_nodes):
            raise ValueError("Cycle detected in dependencies")
            
        zero_indegree_nodes = next_zero_indegree
    
    return layers
