from collections import defaultdict, deque

def resolve_build_order(dependencies):
    # Создаем обратное отображение зависимостей и считаем количество входящих ребер
    incoming_edges = {task: 0 for task in dependencies}
    reverse_dependencies = defaultdict(list)
    
    for task, deps in dependencies.items():
        for dep in deps:
            reverse_dependencies[dep].append(task)  # Зависимость становится предком
            incoming_edges.setdefault(dep, 0)       # Добавляем узел из списка зависимостей
            incoming_edges[task] += 1               # Увеличиваем счетчик входящих ребер
            
    # Ищем все начальные вершины без входящих ребер
    zero_incoming = [task for task, count in incoming_edges.items() if count == 0]
    zero_incoming.sort()
    
    result = []
    queue = deque(zero_incoming)
    
    while queue:
        current_task = queue.popleft()
        result.append(current_task)
        
        # Обновляем входящие ребра у потомков текущего узла
        for dependent in sorted(reverse_dependencies[current_task]):
            incoming_edges[dependent] -= 1
            if incoming_edges[dependent] == 0:
                queue.append(dependent)
                
    # Проверка наличия циклов
    if len(result) != len(incoming_edges):
        raise ValueError("Graph contains cycles")
    
    return result
