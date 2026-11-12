from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # In-degree tracking for topological sorting
    in_degree = defaultdict(int)
    graph = defaultdict(list)
    
    # Build graph and calculate in-degrees
    for dep, deps in dependencies.items():
        for d in deps:
            graph[d].append(dep)
            in_degree[dep] += 1
    
    # Queue of nodes with no dependencies
    queue = deque([node for node, degree in in_degree.items() if degree == 0])
    
    layers = []
    
    while queue:
        # Collect current layer's nodes
        layer_nodes = []
        for _ in range(len(queue)):
            node = queue.popleft()
            layer_nodes.append(node)
        
        # Add current layer to result
        layers.append(sorted(layer_nodes))
        
        # Update in-degrees of dependent nodes
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            
            # If a node becomes free from dependencies, add it to next layer
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # Check for cycles
    if len(layers) != len(in_degree):
        raise ValueError("Cycle detected")
    
    return layers
