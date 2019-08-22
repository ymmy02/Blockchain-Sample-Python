class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        pass
    
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
