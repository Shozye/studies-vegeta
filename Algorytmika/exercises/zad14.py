# Mateusz Pełechaty
# Ćwiczenie 14
# Napisz pseudo-kod algorytmu który otrzymujemy w wyniku derandomizacji wykorzystującej wartość
# oczekiwaną zrandomizowanego algorytmu służącego do wyznaczenia cięcia w grafie (V, E) rozmiaru ­
# E/2.

import random

def amount_edges_between_parts(graph: dict[int, list[int]], V1: list[int], V2: list[int]):
    amount_edges = 0
    for v in V1:
        for v2 in V2:
            if v2 in graph[v]:
                amount_edges += 1
    return amount_edges

def randomized_max_cut(graph: dict[int, list[int]]) -> int:
    """
    Zrandomizowany algorytm na Max Cut
    """
    V1 = []
    V2 = []

    for v in graph.keys():
        if random.random() < 1/2:
            V1.append(v)
        else:
            V2.append(v)
        
    return amount_edges_between_parts(graph, V1, V2)

def derandomized_max_cut(graph: dict[int, list[int]]) -> int:
    """
    Funkcja bedaca zderandomizowanym algorytmem na max cut
    """
    V1 = []
    V2 = []

    for v in graph.keys():
        edges_v_V1 = amount_edges_between_parts(graph, [v], V1)
        edges_v_V2 = amount_edges_between_parts(graph, [v], V2)
        if edges_v_V1 > edges_v_V2:
            V1.append(v)
        else:
            V2.append(v)
    return amount_edges_between_parts(graph, V1, V2)

def main():
    graph: dict[int, list[int]] = {
        # TODO
    }
    print(derandomized_max_cut(graph))

if __name__ == "__main__":
    main()
