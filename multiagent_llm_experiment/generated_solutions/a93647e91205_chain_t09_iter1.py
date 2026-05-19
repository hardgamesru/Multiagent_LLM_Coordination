from collections import deque, defaultdict

def resolve_build_order(dependencies):
    # Track number of incoming edges per node 
    indegree = {task: 0 for task in dependencies}
    
    # Collect all unique tasks including those mentioned only as dependencies
    all_tasks = set()
    for task, deps in dependencies.items():
        all_tasks.add(task)
        for dep in deps:
            all_tasks.add(dep)
            
    # Initialize in-degree count for all unique tasks
    for task in all_tasks:
        if task not in indegree:
            indegree[task] = 0
        
    # Calculate in-degrees based on given dependencies
    for _, deps in dependencies.items():
        for dep in deps:
            indegree[dep] += 1
            
    # Use priority queue to ensure lexicographic order among tasks ready to be processed
    queue = deque(sorted([task for task, degree in indegree.items() if degree == 0]))
    
    result = []
    
    while queue:
        current_task = queue.popleft()
        result.append(current_task)
        
        # Reduce in-degree counts of dependent tasks
        for neighbor in sorted(dependencies.get(current_task, [])):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
                
    # Check for cycles by comparing length of result with total unique tasks
    if len(result) != len(all_tasks):
        raise ValueError('Cycle detected')
    
    return result
