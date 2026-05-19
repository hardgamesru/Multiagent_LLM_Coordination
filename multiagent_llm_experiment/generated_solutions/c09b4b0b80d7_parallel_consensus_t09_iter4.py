from collections import defaultdict, deque

def resolve_build_order(dependencies):
    # Build full set of nodes including those appearing only as dependencies
    all_nodes = set()
    incoming_edges = defaultdict(int)
    
    for node, deps in dependencies.items():
        all_nodes.add(node)
        for dep in deps:
            all_nodes.add(dep)  # Ensure we capture isolated nodes
            incoming_edges[node] += 1  # Count how many other nodes depend on this one
            
    # Create adjacency list representation of the graph
    adj_list = {node: [] for node in all_nodes}
    for node, deps in dependencies.items():
        for dep in deps:
            adj_list[dep].append(node)
        
    # Find starting points with no incoming edges
    queue = deque(sorted([node for node in all_nodes if incoming_edges[node] == 0]))
    
    result = []
    while queue:
        current_node = queue.popleft()  
        result.append(current_node)
        
        # For each dependent node, reduce its incoming edge count
        for neighbor in sorted(adj_list[current_node]):
            incoming_edges[neighbor] -= 1
            if incoming_edges[neighbor] == 0:
                queue.append(neighbor)
                
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
    
    return result
