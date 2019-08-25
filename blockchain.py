from typing import Dict
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify

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
    def hash(block: Dict) -> str:
        """
        Make the hash of Block by SHA-256
        :param block: Block
        :return: str
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        """
        Simple algorithm of the proof of work
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"


app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/transactions/new', methods=['POST'])
def new_transactions():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amounto'])

    response = {'message': f'Transaction was added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    return 'Mine New Block'

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
