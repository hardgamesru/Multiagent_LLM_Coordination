def edit_distance(source: str, target: str) -> int:
    m, n = len(source), len(target)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize first row and column
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
        
    # Fill dynamic programming table
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if source[i-1] == target[j-1] else 1
            
            # Regular operations
            sub = dp[i-1][j-1] + cost
            
            # Deletion/insertion
            del_ins = min(dp[i-1][j] + 1, dp[i][j-1] + 1)
            
            # Transposition check
            if i >= 2 and j >= 2 and \
               source[i-1] == target[j-2] and source[i-2] == target[j-1]:
                transp = dp[i-2][j-2] + cost
                dp[i][j] = min(sub, del_ins, transp)
            else:
                dp[i][j] = min(sub, del_ins)
                
    return dp[m][n]
