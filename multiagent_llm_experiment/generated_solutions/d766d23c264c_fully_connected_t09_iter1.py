from collections import defaultdict, deque

def resolve_build_order(dependencies):
    all_tasks = set()
    for task, deps in dependencies.items():
        all_tasks.add(task)
        all_tasks.update(deps)
    
    adj_list = {task: [] for task in all_tasks}
    indegree_count = {task: 0 for task in all_tasks}
    
    for task, deps in dependencies.items():
        for dep in deps:
            adj_list[dep].append(task)
            indegree_count[task] += 1
    
    ready_queue = deque(sorted([task for task in all_tasks if indegree_count[task] == 0]))
    
    result = []
    
    while ready_queue:
        current_task = ready_queue.popleft()
        result.append(current_task)
        
        for neighbor in sorted(adj_list[current_task]):
            indegree_count[neighbor] -= 1
            if indegree_count[neighbor] == 0:
                ready_queue.append(neighbor)
    
    if len(result) != len(all_tasks):
        raise ValueError("Graph contains a cycle")
    
    return result
