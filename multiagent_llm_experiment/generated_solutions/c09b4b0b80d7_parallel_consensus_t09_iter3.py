from collections import defaultdict, deque

def resolve_build_order(dependencies):
    # Create an adjacency list representation of the graph
    adj = defaultdict(list)
    indegree = {node: 0 for node in dependencies}
    
    # Add reverse edges to capture dependencies properly
    for task, deps in dependencies.items():
        for dep in deps:
            adj[dep].append(task)  # Edge from dependency to dependent task
            indegree.setdefault(dep, 0)  # Ensure all dependencies have entry
            indegree[task] += 1  # Increment incoming edge count for each dependency
            
    # Initialize queue with nodes having no incoming edges
    zero_indegree_nodes = sorted([node for node, degree in indegree.items() if degree == 0])
    queue = deque(zero_indegree_nodes)
    
    result = []
    
    while queue:
        current_node = queue.popleft()
        result.append(current_node)
        
        # Decrease indegree of adjacent nodes and add new zero-indegree nodes
        for neighbor in adj[current_node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
                
    # Check for cycles by comparing length of result with total number of unique nodes
    num_unique_nodes = len(set(indegree.keys()) | set(adj.keys()))
    if len(result) != num_unique_nodes:
        raise ValueError("Graph contains a cycle")
    
    return result
