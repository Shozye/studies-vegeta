import sys



def main(filename: str):
    with open(filename) as file:
        lines = file.read().split("\n")[:-1]
        
    for line in lines:
        n, m, graph_type, P_triangle, P_connected, P_degree4, P_amedges4 = [f(x) for f, x in zip([int, int, str, float, float, float, float], line.split(" "))]
        print(n, m, graph_type, P_triangle, P_connected, P_degree4, P_amedges4)
    
if __name__ == "__main__":
    main(sys.argv[1])
    