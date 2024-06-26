def compute_prefix_function(pattern: str):
    i = 1
    j = 0
    res = [0] * len(pattern)
    # Zlozonosc to O(n), bo if + else wykona sie max len(pattern) razy
    # natomiast elif wykonuje sie gdy j > 0, a j zwiekszamy maksymalnie len(pattern) razy
    while i < len(pattern):
        if pattern[i] == pattern[j]:
            res[i] = j + 1
            i += 1
            j += 1
        elif j > 0:
            # here we have to backtrack to previous
            j = res[j-1]
        else:
            #here suffix start and prefix start do not match so
            # lps[i] = 0 and we move suffix start further
            res[i] = 0
            i += 1
    return res


def kmp(pattern: str, text: str) -> list[int]:
    i,j = 0,0
    answers: list[int] = []
    LPS = compute_prefix_function(pattern)
    while(i < len(text)):
        if(text[i] == pattern[j]):
            i+=1
            j+=1
            if j == len(pattern):
                answers.append(i-j)
                j = LPS[j-1]
        elif j > 0:
            j = LPS[j-1]
        else:
            i+=1
    return answers
    
assert kmp("ana", "analfabetanakondana") == [0,9,16]