"""Ćwiczenie 13
Zaimplementuj metodę ”stratified sampling” 
dla przybliżania wartości całki od a do b z f dx
Przetestuj jej skuteczność na całce od 0 do 1 z √ (1-x**2) dx
Zastosuj możliwie dobry generator liczb pseudo-losowych.

Zastosuj następnie metodę przeciwstawnych elementów (antithetic variaty method) do
wyznaczenia całki od 0 do 1 z √ (1-x**2) dx."""

import math
import random


def f1(x: float) -> float:
    return math.sqrt(1 - x ** 2)

def error(actual, expected):
    return abs(expected - actual) / expected

def sampling(func, a: float, b: float, num_samples=1000) -> float:
    sum_result = 0.0

    for i in range(num_samples):
        sum_result += func(random.uniform(a,b))

    return (b-a) * sum_result / num_samples


def stratified_sampling(func, a: float, b: float, num_samples: int = 1000) -> float:
    sum_result = 0.0
    interval_length = (b - a) / num_samples
    
    for i in range(num_samples):
        xi = random.uniform(a + i * interval_length, a + (i + 1) * interval_length)
        sum_result += func(xi)
    
    integral = sum_result * (b - a) / num_samples
    return integral

def antithetic_variety_method(func, a: float, b: float, num_samples: int = 500) -> float:
    sum_result = 0.0
    
    for _ in range(num_samples):
        u = random.uniform(a, b)
        sum_result += (func(u) + func(1 - u)) / 2
    
    integral = sum_result * (b - a) / num_samples
    return integral
def main():
    goal_value = math.pi / 4

    stratified_value = sampling(f1, 0, 1)
    print(f"Sampling={stratified_value:.6}, \
        error={error(stratified_value, goal_value):.4}")
    
    stratified_value = stratified_sampling(f1, 0, 1)
    print(f"Stratified SamplingMethod={stratified_value:.6}, \
        error={error(stratified_value, goal_value):.4}")
    
    stratified_value = antithetic_variety_method(f1, 0, 1)
    print(f"Antithetic Variety Method={stratified_value:.6}, \
        error={error(stratified_value, goal_value):.4}")
    
    print(f"Expected Value: {goal_value:.4}")

if __name__ == "__main__":
    main()