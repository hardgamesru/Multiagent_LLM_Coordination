from collections import defaultdict

def maximum_matching(adjacency):
    def dfs(v, seen_left, match_right):
        for u in adjacency.get(v, []):
            if u not in match_right or (u in seen_left and dfs(match_right[u], seen_left, match_right)):
                seen_left.add(v)
                match_right[u] = v
                return True
        return False
    
    left_vertices = set(adjacency.keys())
    right_vertices = set()
    for adj_list in adjacency.values():
        right_vertices.update(adj_list)
    
    # If no vertices exist, return 0
    if len(left_vertices) == 0 or len(right_vertices) == 0:
        return 0
    
    match_right = {}
    max_match = 0
    
    # Try each unmatched left vertex
    for v in left_vertices:
        seen_left = set()
        if dfs(v, seen_left, match_right):
            max_match += 1
            
    return max_match
