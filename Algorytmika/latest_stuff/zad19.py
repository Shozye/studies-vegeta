# Mateusz Pełechaty
# Ćwiczenie 19
# Oprogramuj wersję algorytm R Vittera z ciągiem momentów zmian generowanych przed rozpoczęciem
# analizy strumienia danych.

import math
import random

def generate_RVitterMoments(sequence_length: int) -> list[int]:
    next = [1]
    while len(next)< sequence_length:
        last_elem = next[len(next)-1]
        eta = random.random()
        next.append(last_elem + math.ceil((eta * last_elem) /(1 - eta)))
    return next

def main():
    print(generate_RVitterMoments(30))

if __name__ == "__main__":
    main()