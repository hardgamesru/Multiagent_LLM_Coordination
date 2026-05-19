from collections import defaultdict, deque

def resolve_build_order(dependencies):
    # Build full set of nodes (tasks) including those appearing only as dependencies
    all_nodes = set()
    for node, deps in dependencies.items():
        all_nodes.add(node)
        all_nodes.update(deps)
    
    # Compute indegree (number of incoming edges) for each node
    indegree = {node: 0 for node in all_nodes}
    for deps in dependencies.values():
        for dep in deps:
            indegree[dep] += 1
    
    # Initialize queue with nodes having no dependencies
    zero_indegree_queue = deque(sorted([node for node in indegree if indegree[node] == 0]))
    
    result = []
    while zero_indegree_queue:
        current_node = zero_indegree_queue.popleft()
        result.append(current_node)
        
        # Reduce indegree of dependent nodes
        if current_node in dependencies:
            for neighbor in sorted(dependencies[current_node]):
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    zero_indegree_queue.append(neighbor)
    
    # Check for cycles by verifying all nodes were processed
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
    
    return result
