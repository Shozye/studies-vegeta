import sys

from matplotlib import pyplot as plt

suptitles = [
    "P(graf posiada trójkąt?)",
    "P(graf jest spójny?)",
    "P(graf ma połowe wierzchołków stopnia 4?)",
    "P(graf nie ma m wierzchołków)"
]

filenames = [
    "trojkat.png",
    "spojny.png",
    "stopnie.png",
    "nie_m_wierzcholkow.png"
]

def main(filename: str):
    with open(filename) as file:
        lines = file.read().split("\n")[:-1]
        
    data = dict()

    for line in lines:
        n, m, graph_type, P_triangle, P_connected, P_degree4, P_amedges4 = [f(x) for f, x in zip([int, str, str, float, float, float, float], line.split(" "))]
        features = [P_triangle, P_connected, P_degree4, P_amedges4]

        for i in range(len(features)):

            if i not in data:
                data[i] = dict()
            if m not in data[i]:
                data[i][m] = dict()
            if graph_type not in data[i][m]:
                data[i][m][graph_type] = dict()

            data[i][m][graph_type][n] = features[i]

    amount_ms = len(list(data[0].keys()))
    for feature_type in data.keys():
        fig,axs = plt.subplots(amount_ms, 1, constrained_layout=True, figsize=(3, amount_ms*2))
        fig.suptitle(suptitles[feature_type])
        for m_index, m_type in enumerate(data[i].keys()):
            ax = axs[m_index]

            ax.set_title("m="+m_type)
            ax.set_ylim(-0.05,1.05)
            ax.grid(visible=True)

            for graph_type in ["binomial", "uniform"]:
                temp = data[feature_type][m_type][graph_type]
                ax.plot(temp.keys(), temp.values(), label=graph_type, linewidth=2)

                ax.legend()

        fig.savefig(filenames[feature_type])
            
if __name__ == "__main__":
    main(sys.argv[1])
    