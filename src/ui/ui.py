from src.services.user_service import UserService
from src.services.transaction_service import TransactionService
from src.models.user import User

class UI:
    def user_homepage(self, username: str):
        print(f"Welcome, {username}! This is XX store payment card dashboard.")


    def storekeeper_homepage(self):
        print("Storekeeper Dashboard - Manage Transactions")

    def show_payment_confirmation(self, transaction: Transaction):
        print(f"Payment of {transaction.amount} completed using {transaction.payment_method}.")

    def show_updated_balance(self, customer: str, balance: float):
        print(f"{customer}'s new balance: {balance}")