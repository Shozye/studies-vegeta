
import random
from matplotlib import pyplot as plt


def lcs(x: str, y: str):
    # to jakis dp jest. dp[0,0] = 0, dp[0, m] = 0, dp[m, 0] = 0
    # dp[n+1,m+1] = 1 + dp[n][m] if x[n] == x[m]
    # dp[n+1, m+1] = max(dp[n, m+1], dp[n+1, m])
    dp = [[0 for j in range(len(y)+1)] for i in range(len(x)+1)]

    for i in range(len(x)):
        for j in range(len(y)):
            if x[i] == y[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j]) 
    return dp[len(x)][len(y)]

def get_all_binary_sequences(n: int) -> list[str]:
    answer = []
    for i in range(0, 2**n):
        bin_num = bin(i)[2:].zfill(n)
        answer.append(bin_num)
    return answer

def randomized_answer(n: int, tests=10000) -> float:
    binary_seqs = get_all_binary_sequences(5)
    lcs_sum = 0
    for _ in range(tests):
        seq1 = random.choice(binary_seqs)
        seq2 = random.choice(binary_seqs)
        lcs_sum += lcs(seq1, seq2)
    return lcs_sum / tests

def calculated_answer(n: int) -> float:
    binary_seqs = get_all_binary_sequences(n)
    lcs_sum = 0
    for seq1 in binary_seqs:
        for seq2 in binary_seqs:
            lcs_sum += lcs(seq1, seq2)
    return lcs_sum / len(binary_seqs)**2

def main():
    xs = list(range(1, 10))
    ys = []
    for x in xs:
        ys.append(calculated_answer(x))
    
    print(calculated_answer(5))
    plt.plot(xs, ys)
    plt.plot([1,9], [2/3, 6])
    plt.savefig("zad8.png")
    pass
    
if __name__ == "__main__":
    main()
    
    
    
