from collections import defaultdict, deque

def build_layers(dependencies):
    if not dependencies:
        return []
    
    # In-degree tracking for each node
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
        
        # Add layer to result
        layers.append(layer_nodes)
        
        # Update in-degrees and add next layer candidates
        for neighbor in layer_nodes:
            for dependent in graph[neighbor]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
    
    # Check for cycles
    if len(layers) != len(in_degree):
        raise ValueError("Cycle detected")
    
    return layers
