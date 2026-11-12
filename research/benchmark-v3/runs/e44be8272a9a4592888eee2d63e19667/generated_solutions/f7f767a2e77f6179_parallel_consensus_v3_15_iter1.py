from collections import deque

def maximum_matching(adjacency):
    def bfs(start):
        visited = set()
        queue = deque([start])
        while queue:
            u = queue.popleft()
            if u in visited:
                continue
            visited.add(u)
            for v in adjacency.get(u, []):
                if v not in matched or bfs(matched[v]):
                    matched[u] = v
                    return True
            queue.append(u)
        return False
    
    matched = {}
    result = 0
    for u in adjacency.keys():
        if u not in matched:
            bfs(u)
            result += len(matched)//2
    return result * 2
