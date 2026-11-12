def edit_distance(source: str, target: str) -> int:
    m, n = len(source), len(target)
    dp = [[0] * (n+1) for _ in range(m+1)]
    
    # Initialize base cases
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if source[i-1] == target[j-1] else 1
            
            # Standard operations
            insert = dp[i][j-1] + 1
            delete = dp[i-1][j] + 1
            substitute = dp[i-1][j-1] + cost
            
            # Adjacent transpositions
            if i >= 2 and j >= 2 and \
               source[i-1] == target[j-2] and \
               source[i-2] == target[j-1]:
                transpose = dp[i-2][j-2] + 1
                dp[i][j] = min(insert, delete, substitute, transpose)
            else:
                dp[i][j] = min(insert, delete, substitute)
                
    return dp[m][n]
