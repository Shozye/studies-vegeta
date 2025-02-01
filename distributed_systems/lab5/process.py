
from multiprocessing import Process
from multiprocessing.managers import DictProxy, ListProxy
from typing import Optional
from colorama import Fore, Style

from common import Block, Transaction


class Node(Process):
    def __init__(self, node_id: int, network: dict[int, list], lock, difficulty: int):
        super().__init__()
        self.node_id: int = node_id
        self.chain: list[Block] = []     
        self.trans_pool: list[Transaction] = []    
        self.network = network
        self.lock = lock
        self.difficulty: int = difficulty    

    def create_genesis_block(self):
        genesis_block = Block(0, Transaction(-1, -1, -1), "0")
        self.chain.append(genesis_block)
        with self.lock:
            self.network[self.node_id].append(genesis_block)

    def add_transaction(self, transaction: Transaction) -> None:
        self.trans_pool.append(transaction)

    def mine_block(self) -> Optional[Block]:

        trans: Transaction = self.trans_pool.pop(0) 
        
        new_block = Block(
            index=len(self.chain),
            transaction=trans,
            previous_hash=self.chain[-1].hash,
        )

        while not new_block.hash.startswith("0" * self.difficulty):
            new_block.nonce += 1
            new_block.hash = new_block.compute_hash()

            if new_block.nonce % 10000 == 0:
                with self.lock:
                    argmax, longest_chain = self.find_longest_chain_in_lock()
                if len(longest_chain) > len(self.chain):
                    return None

        return new_block

    def add_block(self, block) -> None:
        if block.previous_hash == self.chain[-1].hash:
            self.chain.append(block)

    def find_longest_chain_in_lock(self) -> tuple[int, list]:
        argmax = -1
        longest_chain = []
        for i, lst in enumerate(self.network.values()):
            if len(lst) > len(longest_chain):
                longest_chain = lst
                argmax = i
        return argmax, longest_chain

    def resolve_conflicts(self) -> None:
        with self.lock:
            argmax, longest_chain = self.find_longest_chain_in_lock()

            if len(longest_chain) > len(self.chain):
                self.chain = [b for b in longest_chain]
                self.network[self.node_id] = [b for b in longest_chain] 
                self.trans_pool = self.trans_pool[len(longest_chain) - len(self.chain):]
                print(f"Node {self.node_id}: {Fore.RED}Lost Race with Node{argmax}!{Style.RESET_ALL} My chain(len={len(self.chain)}): {self.chain[-3:]}, Longest chain(len={len(longest_chain)}): {longest_chain[-3:]}")
                print(f"{Fore.GREEN}Node {self.node_id}: I am left with {len(self.trans_pool)} transactions: {self.trans_pool}{Style.RESET_ALL}")
            else:
                print(f"Node {self.node_id}: STILL IN RACE! My chain is size {len(self.chain)}. The same as Node {argmax}")


    def broadcast_block(self, block):
        with self.lock:
            # tutaj informuje wszystkie inne node'y o tym, że dodałem blok do sieci.
            self.network[self.node_id].append(block)

    def run(self):
        self.create_genesis_block() 

        while self.trans_pool: 
            mined_block = self.mine_block() 
            if mined_block is not None:

                print(f"Node {self.node_id} {Fore.CYAN}mined{Style.RESET_ALL} a block: {Fore.CYAN}{mined_block}{Style.RESET_ALL}")
                self.add_block(mined_block)
                self.broadcast_block(mined_block)

            self.resolve_conflicts()
