# Ćwiczenie 20
# Znajdź bibliotekę swojego ulubionego języka programowania która zawiera implementację funkcji MurMurHash. 
# Zastosuj ją do konstrukcji funkcji haszującej h_s w wartościach w zbiorze {0, . . . , 20} dla ziarna s. 
# Zastosuj ją dla ciągu wyrazów ulubionej książki, którą masz zapisaną w formacie ASCII.
# 1. Zbadaj histogram otrzymanych wartości dla kilku różnych wartości ziarna.
# 2. Ustal dwa różne słowa a i b i przetestuj na tych słowach liczbę kolizji h_s(a) = hs(b) dla losowo wybranych 1000 wartości ziarna s

from collections import Counter
import requests
import mmh3

h = mmh3.hash

PAN_TADEUSZ_PATH = "pan_tadeusz.txt"

def main():
    book = set(read_book())

    for seed in range(50):
        hashed = [h(elem, seed) for elem in book]
        ctr = [x[1] for x in Counter(hashed).most_common()]
        freqs = {}
        for freq in [x[1] for x in Counter(hashed).most_common()]:
            freqs[freq] = freqs.get(freq, 0) + 1
    
        print(f"{seed=}, {freqs=}")

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

