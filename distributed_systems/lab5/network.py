
from multiprocessing import Lock, Manager
from process import Node


class BlockchainNetwork:
    def __init__(self, num_nodes, difficulty):
        self.manager = Manager()
        self.network  = self.manager.dict({i: self.manager.list() for i in range(num_nodes)})
        lock = Lock()
        self.nodes: list[Node] = [
            Node(i, self.network, lock, difficulty)  # type: ignore
            for i in range(num_nodes)
        ]

    def start_network(self):
        for node in self.nodes:
            node.start()

    def wait_for_nodes_to_finish(self):
        for node in self.nodes:
            node.join()

    def add_transaction(self, transaction):
        for node in self.nodes:
            node.add_transaction(transaction)
