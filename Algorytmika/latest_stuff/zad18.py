# Mateusz Pełechaty
# Ćwiczenie 18
# Oprogramuj procedurę generowania ciągu chwil w których algorytm R Vittera aktualizuje wartość licznika. 
# Przetestuj ją generując ciągi długości 50.

import random
import time


def generate_RVitterMoments(sequence_length: int) -> list[int]:
    moments = []
    
    st = time.time()

    n = 0
    while len(moments) < sequence_length:
        n += 1
        if random.random() <= 1/n:
            print(f"{len(moments)+1}-th moment: {n} workingtime:{round(time.time()-st)}s")
            moments.append(n)
    
    return moments

def main():
    print(generate_RVitterMoments(30))

if __name__ == "__main__":
    main()