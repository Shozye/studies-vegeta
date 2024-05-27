# Mateusz Pełechaty
# Rozważamy następujący algorytm przybliżonego zliczania liczby stacji w środowisku bezprzewodowym:
# 1. każda stacja v ∈ V generuje niezależnie liczbą losową f(v) ∈ [0, 1];
# 2. zbieramy (nie ważne jak) listę L = {f(v) : v ∈ V };
# 4. jeśli n <= 400 to zwracamy n
# 5. jeśli n > 400 to zwracamy liczbę 399/x_400
# Zbadaj eksperymentalnie dokładność tego algorytmu dla liczby stacji n = 10000

import math
import random

from matplotlib import pyplot as plt


def simulate_stations(amount_stations: int) -> int:
    # 1. każda stacja v ∈ V generuje niezależnie liczbą losową f(v) ∈ [0, 1];
    # 2. zbieramy (nie ważne jak) listę L = {f(v) : v ∈ V };
    L = [random.random() for _ in range(amount_stations)]
    
    # 3. sortujemy listę L i otrzymujemy ciąg x_1 <= x_2 <= . . . <= x_n;
    L.sort()
    
    # 4. jeśli n <= 400 to zwracamy n  (???)
    if amount_stations <= 400:
        return amount_stations
    
    # 5. jeśli n > 400 to zwracamy liczbę 399/x_400
    return int(399 / L[399])

def test(amount_stations: int):
    estimated_stations = simulate_stations(amount_stations)
    error = abs(amount_stations - estimated_stations) / amount_stations
    return error

def run_multiple_average(n, func, *args):
    total = 0
    for _ in range(n):
        total += func(*args)
    return total/n

def main():
    # Przy pokazaniu usun generowanie sie plota
    # To tylko plot pokazujacy blad
    MAX_N = 10000
    xs = list(range(100, MAX_N, 100))
    ys = [run_multiple_average(10, test, x) for x in xs]
    
    plt.plot(xs, ys)
    plt.savefig("zad17_estimator.png")


    # Tutaj sa przykladowe odpalenia
    xs = [1_000, 5_000, 10_000, 20_000, 35_800, 100_000]
    for x in xs:
        print(f"simulate_stations({x})={simulate_stations(x)}")

if __name__ == "__main__":
    main()