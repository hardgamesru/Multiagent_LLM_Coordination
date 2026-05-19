from typing import Dict, List

def resolve_build_order(dependencies: Dict[str, list[str]]) -> List[str]:
    def dfs(node):
        visited.add(node)
        visiting.add(node)  # Mark node as visiting to detect cycles
        
        for neighbor in dependencies.get(node, []):
            if neighbor in visiting:
                raise ValueError("Cycle detected")
            
            if neighbor not in visited:
                dfs(neighbor)
                
        visiting.remove(node)
        result.append(node)
    
    # Create full set of nodes (including those appearing only in dependency lists)
    all_nodes = set()
    for node, deps in dependencies.items():
        all_nodes.add(node)
        all_nodes.update(deps)
    
    sorted_nodes = sorted(all_nodes)  # Lexicographically sort nodes
    visited = set()  
    visiting = set() 
    result = []
    
    for node in sorted_nodes:
        if node not in visited:
            dfs(node)
    
    return result[::-1]
