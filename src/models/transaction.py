class Transaction:
    def __init__(self, username, amount: float, payment_method:str):
        self.username = username
        self.amount = amount
        self.payment_method = payment_method
