from src.models.transaction import Transaction
from src.models.user import User
from typing import List

class TransactionRepository:
    def __init__(self):
        self.transactions = []

    def save_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def fetch_transaction_data(self) -> List[Transaction]:
        return self.transactions


