from copy import deepcopy
import random

class Graph:
    graph: dict[int, list[int]]
    
    def __init__(self, graph: dict[int, list[int]]) -> None:
        self.graph = graph
        self.highest_node = 0
    
    def clone(self):
        return Graph(deepcopy(self.graph))
    
    def add_node(self, u: int):
        self.graph[u] = list()
        if u > self.highest_node:
            self.highest_node = u
        
    def get_amount_edges(self) -> int:
        amount_edges = 0
        for edges in self.graph.values():
            amount_edges += len(edges)
        return amount_edges
    
    def add_edge(self, u: int, v: int):
        self.graph[u].append(v)
    
    def contract_edge(self, u: int, v: int):
        edges_of_uv: list[int] = list()
        for e in self.graph[u]:
            if e != v:
                edges_of_uv.append(e)
        for e in self.graph[v]:
            if e != u:
                edges_of_uv.append(e)
        
        uv_node: int = self.highest_node+1
        self.highest_node += 1
        del self.graph[u]
        del self.graph[v]
        for edges in self.graph.values():
            for i, target in enumerate(edges):
                if target == u or target == v:
                    edges[i] = uv_node
        
        self.graph[uv_node] = edges_of_uv
    
    def get_random_edge(self) -> tuple[int, int]:
        amount_edges: int = self.get_amount_edges()
        random_edge_index: int = random.randrange(0, amount_edges)
        for u, edges in self.graph.items():
            if len(edges) < random_edge_index:
                return (u, edges[random_edge_index])
            random_edge_index -= len(edges)

        raise Exception("?")


def karger_min_cut(g: Graph) -> int:
    graph = g.clone()
    while len(graph.graph) > 2:
        u, v = graph.get_random_edge()
        graph.contract_edge(u, v)
    return len(list(graph.graph.values())[0])
    