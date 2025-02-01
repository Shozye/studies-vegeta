import random
from common import Transaction
from network import BlockchainNetwork


def main():
    NUM_NODES = 5
    NUM_TRANSACTIONS = 20
    DIFFICULTY = 6

    blockchain_network = BlockchainNetwork(NUM_NODES, DIFFICULTY)
    for _ in range(NUM_TRANSACTIONS):
        transaction = Transaction(
            sender=random.randint(0, NUM_NODES - 1), 
            receiver=random.randint(0, NUM_NODES - 1), 
            amount=random.randint(1, 100)
        )
        blockchain_network.add_transaction(transaction)

    blockchain_network.start_network()
    print ("Network start")
    blockchain_network.wait_for_nodes_to_finish()
    print ("Network stop")

if __name__ == "__main__":
    main()