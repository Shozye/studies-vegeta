# Mateusz Pełechaty
# Ćwiczenie 15
# Rozważmy algorytm sużący wygenerowania ciągu długości n składającego się z samych zer:
# for i = 1 to n {
#   X[i] = randomBit
# }
# return X
# Prawdopodobieństwo sukcesu tego algorytmu wynosi 1 / 2**n
# Przeprowadź derandomizację tego algorytmu metodą prawdopodobieństw warunkowych, 
# czyli rozważ ciąg funkcji c(x1, . . . , xk) = Pr[Sukces|X1 = x1, . . . , Xk = xk] .

def derandomize_sequence(n: int) -> list:
    sequence = []
    
    for i in range(n):
        # Prawdopodobieństwo sukcesu, gdy X[i] = 0
        prob_if_zero = 1 / 2 ** (n - i - 1)
        
        # Prawdopodobieństwo sukcesu, gdy X[i] = 1
        prob_if_one = 0  # Bo jeśli ustawimy 1, nie możemy mieć ciągu samych zer
        
        if prob_if_zero >= prob_if_one:
            sequence.append(0)
        else:
            sequence.append(1)
    
    return sequence

def main():
    n = 10  # Przykładowa długość ciągu
    sequence = derandomize_sequence(n)
    print(f"Wygenerowany ciąg: {sequence}")
    print(f"Sukces: {'Tak' if all(x == 0 for x in sequence) else 'Nie'}")

if __name__ == "__main__":
    main()