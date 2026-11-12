from collections import defaultdict

def maximum_matching(adjacency):
    def dfs(v, visited_left, match_right):
        for u in adjacency.get(v, []):
            if not match_right[u]:
                # Try to assign current vertex from left to current vertex from right
                match_right[u] = v
                return True
            elif u not in visited_left:
                # Explore unvisited right vertices recursively
                visited_left.add(v)
                if dfs(match_right[u], visited_left, match_right):
                    # Found a valid assignment, update mapping
                    match_right[u] = v
                    return True
        return False

    # Track which right vertices were matched
    match_right = {}
    
    # Iterate through each left vertex
    for v in adjacency.keys():
        visited_left = set()
        # Perform DFS search starting from current left vertex
        if dfs(v, visited_left, match_right):
            # Increment count of matched pairs
            pass  # No explicit counter needed as we modify dictionary directly

    # Count total number of matches
    return len(match_right)
