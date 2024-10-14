import cProfile
from collections import defaultdict
import json
import math
import random
from collections import deque

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
        
class UniformGraph(Graph):
    def __init__(self, n: int, m: int) -> None:
        super().__init__(n)
        self.generate_uniform_edges(m)
        self.name = "uniform"
        
    def generate_uniform_edges(self, m: int) -> None:
        try:
            for u, v in random.sample(self.possible_edges, k=m):
                self.add_edge(u, v)
        except ValueError:
            print(f"Error: {self.possible_edges=}, {m=}")
            raise

        

class BinomialGraph(Graph):
    def __init__(self, n: int, p: float) -> None:
        super().__init__(n)
        self.generate_binomial_edges(p)
        self.name = "binomial"

    def generate_binomial_edges(self, p: float):
        for u, v in self.possible_edges:
            if random.random() < p:
                self.add_edge(u, v)


def has_at_least_one_triangle(g: Graph) -> bool:
    for v1 in range(len(g.edges)):
        for v2 in g.edges[v1]:
            for v3 in range(len(g.edges)):
                if v1 in g.edges[v3] and v2 in g.edges[v3]:
                    return True
    return False

def is_connected(g: Graph) -> bool:
    visited = set([0])
    queue = deque([0])
    while queue:
        v = queue.popleft()
        for neigh in g.edges[v]:
            if neigh not in visited:
                queue.append(neigh)
                visited.add(neigh)
    return len(visited) == g.n

def has_half_of_vertices_with_degree_4(g: Graph) -> bool:
    amount_of_vertices_with_degree_4 = 0
    for edges in g.edges:
        if len(edges) >= 4:
            amount_of_vertices_with_degree_4 += 1
    return amount_of_vertices_with_degree_4 >= g.n / 2

def has_amount_edges_different_than_m(m: int, g: Graph) -> bool:
    return m != (sum(len(edges) for edges in g.edges) / 2)

def binom_n_2(n: int) -> float:
    return n * (n-1) / 2


def main():
    ns_tested = [5] + list(range(10, 400, 50))
    possible_ms = [
        (lambda n: math.sqrt(n), "sqrt(n)"),
        (lambda n: n, "n"),
        (lambda n: 2*n, "2n"),
        (lambda n: n * math.log2(n), "n*log2(n)"),
        (lambda n: (1/4) * n**2, "1/4n**2")
    ]
    data = dict()
    print_string = ""
    
    for possible_m, m_name in possible_ms:
        for n in ns_tested:
            m = int(possible_m(n))
            if m > binom_n_2(n):
                continue
            p = m / binom_n_2(n)
            
            features = [
                has_at_least_one_triangle,
                is_connected,
                has_half_of_vertices_with_degree_4,
                lambda g: has_amount_edges_different_than_m(m, g)
            ]
            
            print(f"Doing tests for {n=}, {m=}")
            for g in [lambda: UniformGraph(n, m), lambda: BinomialGraph(n, p)]:
                
                AMOUNT_TESTS = 100
                for _ in range(AMOUNT_TESTS):
                    graph = g()
                    graph_features = [f(graph) for f in features]
                    
                
                    if n not in data:
                        data[n] = dict()
                    if m_name not in data[n]:
                        data[n][m_name] = dict()
                        
                    if g not in data[n][m_name]:
                        data[n][m_name][graph.name] = graph_features
                    else:
                        for i in range(len(graph_features)):
                            data[n][m_name][graph.name][i] += graph_features[i]
                
                for i in range(len(data[n][m_name][graph.name])):
                    data[n][m_name][graph.name][i] /= AMOUNT_TESTS
                
                print_string += f"{n} {m_name} {g} {' '.join([str(x) for x in data[n][m_name][graph.name]])}\n"
    
    with open("data.txt", 'w+') as file:
        file.write(print_string)
                
if __name__ == "__main__":
    main()