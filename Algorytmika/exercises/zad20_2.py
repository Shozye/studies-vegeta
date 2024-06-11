# Ćwiczenie 20
# Znajdź bibliotekę swojego ulubionego języka programowania która zawiera implementację funkcji MurMurHash. 
# Zastosuj ją do konstrukcji funkcji haszującej h_s w wartościach w zbiorze {0, . . . , 20} dla ziarna s. 
# Zastosuj ją dla ciągu wyrazów ulubionej książki, którą masz zapisaną w formacie ASCII.
# 1. Zbadaj histogram otrzymanych wartości dla kilku różnych wartości ziarna.
# 2. Ustal dwa różne słowa a i b i przetestuj na tych słowach liczbę kolizji h_s(a) = hs(b) dla losowo wybranych 1000 wartości ziarna s

import requests
import random
import mmh3

h = lambda v, s: mmh3.hash(v, s) % 21

def main():
    w1 = "book"
    w2 = "pantadeusz"
    AMOUNT_TESTS=1000
    
    seeds = [random.randrange(1, 1_000_000) for _ in range(AMOUNT_TESTS)]
    collisions = []

    for seed in seeds:
        h1 = h(w1, seed)
        h2 = h(w2, seed)
        if h1 == h2:
            collisions.append(seed)

    print(f"{collisions=}")
    print(f"{len(collisions)=}")
    
    print("Oczekiwana liczba kolizji: ", AMOUNT_TESTS / 21)


if __name__ == "__main__":
    main()

