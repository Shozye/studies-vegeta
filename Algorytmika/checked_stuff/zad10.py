# Mateusz Pełechaty
# Ćwiczenie 10
# Zaimplementuj algorytm wyznaczania 
# najdłuższego wspólnego podciągu dla trzech ciągów

def longest_common_subsequence(
    s1: str, 
    s2: str, 
    s3: str
) -> int:
    dp = [
        [
            [0] * (len(s3) + 1)
            for _ in range(len(s2)+1)
        ] 
        for _ in range(len(s1)+1)
    ]
    
    for i1 in range(len(s1) + 1):
        for i2 in range(len(s2) + 1):
            for i3 in range(len(s3) + 1):
                if i1 == 0 or i2 == 0 or i3 == 0:
                    dp[i1][i2][i3] = 0
                elif s1[i1-1] == s2[i2-1] == s3[i3-1]:
                    dp[i1][i2][i3] = dp[i1 - 1][i2 - 1][i3 - 1] + 1
                else:
                    dp[i1][i2][i3] = max(
                        dp[i1-1][i2][i3], 
                        dp[i1][i2-1][i3], 
                        dp[i1][i2][i3-1]
                    )
    return dp[len(s1)][len(s2)][len(s3)]

def main():
    assert longest_common_subsequence("AGGT12", "12TXAYB", "12XBA") == 2
    assert longest_common_subsequence("abcd1e2", "bc12ea", "bd1ea") == 3
    assert longest_common_subsequence("abc", "abc", "abc") == 3
    assert longest_common_subsequence("abc", "def", "ghi") == 0
    assert longest_common_subsequence("", "", "") == 0
    assert longest_common_subsequence("a", "a", "a") == 1
    assert longest_common_subsequence("abcdef", "abc", "def") == 0

    print("Tests passed")


if __name__ == "__main__":
    main()
