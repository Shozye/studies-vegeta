
def get_prefix_suffix(w1: str, w2: str) -> int:
    k: int = min(len(w1), len(w2))
    while not w2.endswith(w1[:k]) and k != 0:
        k -= 1
    return k

def main():
    assert get_prefix_suffix("rzysztof", "patrzy") == 3
    assert get_prefix_suffix("janoqfn", "asccspogerja") == 2

