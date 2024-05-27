# Mateusz Pełechaty
# Power of Two Choices. Rozważamy dwa procesy losowej alokacji m = 10^6 kul do n = 10^3 kubełków.
# Oprogramuj te procesy, przeprowadź symulacje i wygeneruj histogramy alokacji kul w kubełkach.
# 1. W pierwszym procesie każdą kulę umieszczamy w losowo (rozważamy rozkład jednostajny), niezależnie wybranych kubełkach.
# 2. W drugim procesie stosujemy metodę Dwóch Wyborów.

import random

from matplotlib import pyplot as plt


def random_simulate(amount_balls: int, amount_bins: int):
    bins = [0] * amount_bins
    
    for _ in range(amount_balls):
        chosen_bin = random.randint(0, amount_bins - 1)
        bins[chosen_bin] += 1
    
    return bins

def two_choices_simulate(amount_balls: int, amount_bins: int):
    # TWO CHOICES - losujemy dwa kosze i wybiermay ten z mniejsza iloscia kul
    bins = [0] * amount_bins
    
    for _ in range(amount_balls):
        bin1 = random.randint(0, amount_bins - 1)
        bin2 = random.randint(0, amount_bins - 1)
        if bins[bin1] < bins[bin2]:
            bins[bin1] += 1
        else:
            bins[bin2] += 1
    
    return bins

def plot_histogram(data: list[int], title: str):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=range(min(data), max(data) + 1), edgecolor='black')
    plt.title(title)
    plt.xlabel('Number of Balls in Bin')
    plt.ylabel('Amount of Bins with X amount of balls')
    plt.grid(True)
    plt.savefig(f"zad16_histogram_{title}.png")

def main():
    m = 10**6
    n = 10**3
    
    # Simulate the random process
    random_bins = random_simulate(m, n)
    plot_histogram(random_bins, 'Random Allocation of Balls into Bins')
    
    # Simulate the Two Choices process
    two_choices_bins = two_choices_simulate(m, n)
    plot_histogram(two_choices_bins, 'Two Choices Allocation of Balls into Bins')

if __name__ == "__main__":
    main()