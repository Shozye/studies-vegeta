
def lcs(x: str, y: str):
    # to jakis dp jest. dp[0,0] = x[0] == y[0]
    # dp[n+1,m+1] = 1 + dp[n][m] if x[n] == x[m]
    # dp[n+1, m+1] = max(dp[n, m+1], dp[n+1, m])
    dp = [[0 for j in range(len(y)+1)] for i in range(len(x)+1)]

    for i in range(len(x)):
        for j in range(len(y)):
            dp[i+1][j+1] = 1+dp[i][j]
    
    
