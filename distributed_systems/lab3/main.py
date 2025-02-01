import logging
import math
from queue import SimpleQueue
import time
from src.snapshot import SnapshotManager
from src.process import Process

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm
from matplotlib import colors as mcolors
from matplotlib import axes
from matplotlib import colormaps
import os
from PIL import Image
# print(mcolors.get_named_colors_mapping())
# NODE_CMAP = mcolors.LinearSegmentedColormap.from_list("WGR",colors = [(0.00, "white"), (0.03, "white"),  (0.10, "green"), (1.00, "red")])
NODE_CMAP = colormaps.get('Wistia')

EDGE_CMAP = mcolors.LinearSegmentedColormap.from_list("BR", [(0, "black"), (1, "red")])


def check_good_snapshot(snapshot: dict, expected_number_of_resources: int):
    resources_in_processes = 0
    for process_data in snapshot['processes'].values():
        resources_in_processes += process_data['resources']
    resources_in_channels = 0
    for channel_data in snapshot['channels'].values():
        resources_in_channels += len(channel_data)
    try:
        assert resources_in_processes + resources_in_channels == expected_number_of_resources
    except:
        print("Error", resources_in_processes + resources_in_channels, '!=', expected_number_of_resources)



def make_the_plot(snapshot_queue:SimpleQueue[dict], vertices: list[int], edges: list[tuple[int, int]], amount_resources: int):
    G = nx.DiGraph()
    for v in vertices:
        G.add_node(v)
    for u, v in edges:
        G.add_edge(u, v)
    pos = nx.spring_layout(G, k=2/math.sqrt(len(vertices)))

    node_norm = mcolors.Normalize(vmin=0, vmax=amount_resources)

    _, ax = plt.subplots(figsize=(8, 8))

    def draw_snapshot(snapshot):
        ax.clear()

        node_colors = []
        labels = {}
        for v in vertices:
            data = snapshot['processes'][str(v)]
            node_colors.append(NODE_CMAP(node_norm(data['resources']))) # type: ignore
            labels[v] = f"{v}\n{data['resources']}"

        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=800) # type: ignore
        nx.draw_networkx_labels(G, pos, labels, font_size=10, ax=ax)

        # Draw edges with message counts
        edge_labels = {}
        for edge, messages in snapshot['channels'].items():
            src, dest = map(int, edge.split('->'))
            edge_labels[(src, dest)] = f"{len(messages)}"


        nx.draw_networkx_edges(G,
                                pos,
                                ax=ax,
                                #  connectionstyle='arc3,rad=0.2',
                                arrowstyle='-|>',
                                arrowsize=30
        )

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels,
            label_pos=0.85,
            font_size=11,
            ax=ax,
        )

        ax.set_title(f"Snapshot: Marker {snapshot['marker_id']}", fontsize=14)
        ax.axis('off')
    

    frames = []
    for _ in range(20):
        snapshot = snapshot_queue.get()
        check_good_snapshot(snapshot, amount_resources)
        draw_snapshot(snapshot)

        # Save the current frame to a temporary file
        temp_file = f"frame_{snapshot['marker_id']}.png"
        plt.savefig(temp_file)
        frames.append(temp_file)
    
        # Combine frames into a GIF using PIL
    images = [Image.open(frame) for frame in frames]
    images[0].save("out.gif", save_all=True, append_images=images[1:], duration=1000, loop=0)

    # Clean up temporary files
    for frame in frames:
        os.remove(frame)




def main():
    logging.basicConfig(level=logging.ERROR)

    vertices = [0, 1, 2, 3, 4, 5,6,7]
    resources = [10,10,10,10,10,10,10, 0]
    edges = []
    for i in range(7):
        for j in range(i+1, 7):
            edges.append((i,j))
            edges.append((j,i))
    edges.append((6,7))
    edges.append((7,6))

    processes = [Process(pid=pid, amount_resources=amount_resources) for pid, amount_resources in zip(vertices, resources)]
    processes[7].set_should_not_send_resources()

    for pid_from, pid_to in edges:
        Process.connect(processes[pid_from], processes[pid_to])

    snapshot_queue = SimpleQueue()
    snapshot_manager = SnapshotManager(snapshot_queue)
    for p in processes:
        snapshot_manager.connect_to_process(p)

    for p in processes:
        p.start()
    snapshot_manager.start()
    make_the_plot(snapshot_queue, vertices, edges, sum(resources))


if __name__ == "__main__":
    main()