from dataclasses import dataclass
import hashlib


@dataclass
class Transaction:
    sender: int
    receiver: int
    amount: int

class Block:
    def __init__(self, index: int, transaction: Transaction, previous_hash: str, nonce=0):
        self.index = index
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_data = str(self.index) + str(self.transaction) + self.previous_hash + str(self.nonce)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"Block(index={self.index}, transactions={str(self.transaction)}, prev_hash={self.previous_hash[:15]}..., hash={self.hash[:15]}..., nonce={self.nonce})"