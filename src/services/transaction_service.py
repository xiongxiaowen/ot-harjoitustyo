from src.models.user import User
from src.repositories.transaction_repository import TransactionRepository
from src.models.transaction import Transaction
from src.repositories.user_repository import UserRepository
from datetime import datetime

class TransactionService:
    """Service layer for processing all transaction business logics.

    Acts as the mid layer between user operations and repositories, execute
    loading money, process payment, and fetch transaction data. 
    """
    def __init__(self, transaction_repo=None, user_repo=None):
        self.transaction_repo = transaction_repo or TransactionRepository()
        self.user_repo = user_repo or UserRepository()
        self.discount = 0.1 #Pay with membership card gets 10% discount

    def load_money_to_card(self, username, amount):
        """Load money to customer's card by storekeeper, amount can not be negative.
        
        Args: 
            username (str): The username of the customer
            amount (float): the amount to load (positive)
        """
        if amount <= 0:
            return False
        return self.user_repo.update_balance(username, amount)

    def process_payment(self, username, amount, payment_method): 
        """Process payment operations by storekeeper. 
        
        Applies discount to card payment, check sufficient balance, store payment transaction
        into database.

        Args: 
            username (str): The username of the customer
            amount (float): the amount to load (float, positive) 
            payment_method (str): either card or cash

        Retuns: 
            Transaction

        Raises: 
            ValueError: If amount not positive or insufficient card balance
            Exception: if user not found or database operation fails          
        """

        if amount <= 0:
            raise ValueError("Amount must be positive")

        final_amount = amount
        if payment_method == "card": 
            final_amount = amount * (1 - self.discount)
            balance = self.user_repo.get_balance(username)
            if balance < final_amount:
                raise ValueError("Not sufficient balance to pay after discount!")

            #update balance with discounted final price
            self.user_repo.update_balance(username, -final_amount)

        #create and save the transaction as final amount
        user = self.user_repo.find_user_by_username(username)
        transaction = Transaction(user.user_id, final_amount, payment_method, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.transaction_repo.save_transaction(transaction)
        return transaction


    def get_customer_transactions(self, username):
        """Get transaction history for a specific customer

        Args:
            username (str): the customer per query

        Returns:
            list: list of date, amount and method through method get_transactions_by_username.
        """
        return self.transaction_repo.get_transactions_by_username(username)

    def get_transaction_history(self):
        """Return all transaction records stored in database. for storekeeper."""
        return self.transaction_repo.get_all_transactions()

    def get_total_revenue(self):
        """Calculate total revenue from card and cash payments. for storekeeper."""
        return self.transaction_repo.get_total_revenue()

    def get_cash_register_balance(self):
        """Calculate total cash received from customers. for storekeeper."""
        return self.transaction_repo.get_cash_register_balance()
