from collections import defaultdict, deque

def resolve_build_order(dependencies):
    # Create adjacency list representation of the graph
    adj = {task: deps[:] for task, deps in dependencies.items()}
    
    # Find incoming edges count for each node
    in_degree = defaultdict(int)
    for dep_list in adj.values():
        for dep in dep_list:
            in_degree[dep] += 1
            
    # Add nodes with no incoming edges to queue 
    start_nodes = sorted([node for node in adj.keys() if in_degree[node] == 0])
    q = deque(start_nodes)
    
    result = []
    
    while q:
        current_node = q.popleft()
        result.append(current_node)
        
        # Decrease degree of neighbors and add new nodes with zero degree
        for neighbor in adj[current_node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)
                
    # Check if there is a cycle by comparing length of result with total number of unique nodes
    all_nodes = set(adj.keys())
    for values in adj.values():
        all_nodes.update(values)
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
    
    return result
