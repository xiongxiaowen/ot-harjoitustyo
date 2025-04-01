from src.models.transaction import Transaction
from src.models.user import User
from typing import List

class TransactionRepository:
    def __init__(self):
        self.transactions = []
        self.user_balances = {}

    def save_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def fetch_transaction_data(self) -> List[Transaction]:
        return self.transactions

    def update_customer_balance(self, customer: User, amount: float):
        #update the card balance
        self.customer_balances[customer] = self.customer_balances.get(customer, 0) + amount

