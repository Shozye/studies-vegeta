import random
import math
from matplotlib import pyplot as plt

def monte_carlo(sample: int=1000) -> float:
    
    counter: int = 0
    for _ in range(sample):
        r1 = random.random()*math.pi
        r2 = random.random()
        
        if r2 < math.sin(r1):
            counter += 1
    
    answer = (counter / sample) * math.pi
    #print(f"Approximately: {sample=}, {counter=}, {answer=}")
    return answer
    
def error(actual: float, expected: float) -> float:
    return abs(actual - expected) / expected

def avg(x: list[float]) -> float:
    return sum(x)/len(x)

def main():
    X = list(range(10,10001, 10))
    Y: list[float] = []
    for x in X:
        Y.append(avg([error(monte_carlo(x), 2) for _ in range(10)]))
    
    plt.plot(X, Y) # type: ignore
    plt.savefig("zad8.png") # type: ignore
    
if __name__ == "__main__":
    main()
