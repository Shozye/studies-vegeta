import math
import matplotlib.pyplot as plt

def v(n, r):
    pie = math.pi ** (n / 2)
    rn = r ** n
    
    gama = math.gamma(n/2 + 1)
    return pie * rn / gama

vals = dict()
rs = [0.5, 1, 2]
for r in rs:
    vals[r] = []
    
ns = list(range(1, 51))

for r in rs:
    for n in ns:
        vals[r].append(v(n, r))

print(vals)

for r in rs:
    plt.plot(vals[r], label=f"r={r}")
    plt.legend()
    plt.grid(visible=True, which='both')
    plt.savefig(f"volube_ball_r={r}.png")
    plt.clf()

