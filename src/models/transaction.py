#improvement from previous codes: added date for storing transaction history

class Transaction:
    def __init__(self, user_id, amount, payment_method, date):
        self.user_id = user_id
        self.amount = amount
        self.payment_method = payment_method
        self.date = date
