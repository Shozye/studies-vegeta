import math
import random

class Graph:
    edges: list[list[int]]
    n: int
    
    def __init__(self, n: int) -> None:
        self.n = n
        self.possible_edges = [(u,v) for u in range(self.n) for v in range(u+1, self.n)]
        self.edges = [[] for _ in range(self.n)]
        
    def add_edge(self, u, v):
        self.edges[u].append(v)
        self.edges[v].append(u)
        
class ErdosRenyiGraph(Graph):
    def __init__(self, n: int, m: int) -> None:
        super().__init__(n)
        self.generate_edges(m)
        
    def generate_edges(self, m: int) -> None:
        for u, v in random.sample(self.possible_edges, k=m):
            self.add_edge(u, v)

class BinomialGraph(Graph):
    def __init__(self, n: int, p: float) -> None:
        super().__init__(n)
        self.generate_binomial_edges(p)

    def generate_binomial_edges(self, p: float):
        for u, v in self.possible_edges:
            if random.random() < p:
                self.add_edge(u, v)


def has_at_least_one_triangle(g: Graph) -> bool:
    raise NotImplementedError()

def is_connected(g: Graph) -> bool:
    raise NotImplementedError()

def has_half_of_vertices_with_degree_4(g: Graph) -> bool:
    raise NotImplementedError()

def has_amount_edges_different_than_m(m: int, g: Graph) -> bool:
    raise NotImplementedError()

def binom_n_2(n: int) -> float:
    return n * (n-1) / 2


def main():
    ns_tested = [1,3,5] + list(range(10, 10, 10)) + list(range(100, 1001, 50))
    possible_ms = [
        lambda n: int(math.log(n)),
        lambda n: n,
        lambda n: int(math.sqrt(n) * n),
        lambda n: n**2
    ]
    
    for possible_m in possible_ms:
        for n in ns_tested:
            m = possible_m(n)
            p = m / binom_n_2(n)
            
            features = [
                has_at_least_one_triangle,
                is_connected,
                has_half_of_vertices_with_degree_4,
                lambda g: has_amount_edges_different_than_m(m, g)
            ]
            
            for g in [ErdosRenyiGraph(n, m), BinomialGraph(n, p)]:
                pass
            
                