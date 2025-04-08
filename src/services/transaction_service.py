from src.models.user import User
from src.repositories.transaction_repository import TransactionRepository
from src.models.transaction import Transaction
from typing import List

class TransactionService:
    def __init__(self, transaction_repo: TransactionRepository):
        self.transaction_repo = transaction_repo
        self.discount = 0.1 #pay with membership card gets 10% discount

    def load_money_to_card(self, customer: User, amount: float):
        #Load money to customer's card, amount can not be negative
        if amount <= 0:
            return False
        return self.transaction_repo.update_customer_balance(customer, amount)

    def process_payment(self, customer: User, amount: float, payment_method:str): 
        #payment from customer to storekeeper, reduce card balance, amount can not be negative
        #apply discount before updating balance 

        if amount <= 0:
            raise ValueError("Amount must be positive")

        final_amount = amount
        if payment_method == "card": 
            final_amount = amount * (1 - self.discount)
            if self.transaction_repo.customer_balances.get(customer, 0) < final_amount:
                raise ValueError("Not sufficient balance to pay after discount!")

            #update balance with discounted final price
            self.transaction_repo.update_customer_balance(customer, -final_amount)

        #create and save the transaction as final amount
        transaction = Transaction(customer, final_amount, payment_method)
        self.transaction_repo.save_transaction(transaction)          
        return transaction

    def get_transaction_history(self) -> List[Transaction]:
        #obtain all transactions
        return self.transaction_repo.fetch_transaction_data()