from collections import defaultdict, deque

def build_layers(dependencies):
    in_degree = defaultdict(int)
    graph = defaultdict(list)
    
    # Build graph and calculate in-degree for each node
    for node, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(node)
            in_degree[node] += 1
    
    # Initialize queue with nodes that have no dependencies
    zero_indegree_nodes = deque([node for node, degree in in_degree.items() if degree == 0])
    
    # List to store layers of nodes
    result = []
    
    while zero_indegree_nodes:
        # Collect current layer nodes
        layer = sorted(zero_indegree_nodes)
        
        # Add current layer to result
        result.append(layer)
        
        # Remove processed nodes from in-degree tracking
        for node in layer:
            del in_degree[node]
            
            # Update in-degree of dependent nodes
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                
                # If a dependent node becomes free, add it to next layer
                if in_degree[neighbor] == 0:
                    zero_indegree_nodes.append(neighbor)
    
    # Check for cycles by verifying if there are unprocessed nodes left
    if len(in_degree) != 0:
        raise ValueError("Cycle detected in dependencies")
    
    return result
