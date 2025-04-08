#improvement from previous codes: added date for storing transaction history
from datetime import datetime

class Transaction:
    def __init__(self, user_id: int, amount: float, payment_method:str, datetime: str=None):
        self.user_id = user_id #use ID identify user instead of username
        self.amount = amount
        self.payment_method = payment_method
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
