# Ćwiczenie 20
# Znajdź bibliotekę swojego ulubionego języka programowania która zawiera implementację funkcji MurMurHash. 
# Zastosuj ją do konstrukcji funkcji haszującej h_s w wartościach w zbiorze {0, . . . , 20} dla ziarna s. 
# Zastosuj ją dla ciągu wyrazów ulubionej książki, którą masz zapisaną w formacie ASCII.
# 1. Zbadaj histogram otrzymanych wartości dla kilku różnych wartości ziarna.
# 2. Ustal dwa różne słowa a i b i przetestuj na tych słowach liczbę kolizji h_s(a) = hs(b) dla losowo wybranych 1000 wartości ziarna s

from collections import Counter
from matplotlib import pyplot as plt
import requests
import mmh3

h = lambda v, s: mmh3.hash(v, s) % 21

PAN_TADEUSZ_PATH = "pan_tadeusz.txt"


def main():
    book = set(read_book())

    for seed in [5,9,24,6624]:
        hashed = [h(elem, seed) for elem in book]
        #print(hashed)
        
        ctr = (Counter(hashed).most_common())
        xs_ys = sorted(ctr, key=lambda x: x[0])
        xs = [str(x[0]) for x in xs_ys]
        ys = [x[1] for x in xs_ys]
        plt.plot(xs, ys)

        plt.ylim(0, 2000)
        plt.savefig(f"zad20_1_seed={seed}")
    

def setup_pan_tadeusz():
    url = "https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt"
    with open(PAN_TADEUSZ_PATH, 'wb') as file:
        response = requests.get(url)
        file.write(response.content)

def read_book():
    with open(PAN_TADEUSZ_PATH) as file:
        book = file.read()
    
    book = book.split()
    return book

if __name__ == "__main__":
    setup_pan_tadeusz()
    main()

