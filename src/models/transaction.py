"""Creat transaction to handle all business logics relating to transaction history"""

class Transaction:
    """Represents a transaction generated in the system.
    
    Attributes:
        user_id (int): Unique identifier of the user associated with the transaction
        amount (float): value of the transaction
        payment_method (str): Method used for payment (either 'card' or'cash')
        date (datetime): Timestamp of when the transaction occurred
    """
    def __init__(self, user_id, amount, payment_method, date):
        self.user_id = user_id
        self.amount = amount
        self.payment_method = payment_method
        self.date = date
