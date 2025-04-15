#updated based on two user roles: customer and storekeeper (admin)

class User:
    def __init__(self, user_id = None, username= "", password= "", role= "customer", balance= 0.0):
        self.user_id = user_id  #meaning "id" in DB
        self.username = username
        self.password = password
        self.role = role  #customer or storekeeper(admin)
        self.balance = balance

    def is_storekeeper(self): 
        return self.role == "storekeeper"

    def is_customer(self): 
        return self.role == "customer"
