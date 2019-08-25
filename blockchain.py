from typing import Dict
import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self, proof: int, previous_hash: str=None) -> Dict:
        """
        :param proof: Proof from the proof of work algorithm
        :param previous_hash: (Option) Hash of previous hash
        :return: New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """
        :param sender: Address of Sender
        :param recipient: Address of Recipient
        :param amount: Amount
        :return: Address of Block which includes this Transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        pass

    @property
    def last_block(self):
        pass
