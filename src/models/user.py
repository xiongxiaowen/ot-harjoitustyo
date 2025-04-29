"""This class for managing user info and roles, representing a user in the system."""


class User:
    """Defind user and user roles
     
    Attributes:
        user_id (int): Unique identifier for the user in DB. Defaults to None.
        username (str): User's username for authentication. Defaults to empty string.
        password (str): User's password for authentication. Defaults to empty string.
        role (str): User's role, either 'customer' or 'storekeeper'. Defaults to 'customer'.
        balance (float): User's account balance. Defaults to 0.0. 
    """
    def __init__(self, user_id = None, username= "", password= "", role= "customer", balance= 0.0):
        self.user_id = user_id  #meaning "id" in DB
        self.username = username
        self.password = password
        self.role = role  #customer or storekeeper(admin)
        self.balance = balance

    def is_storekeeper(self):
        """Check if user is storekeeper
        
        Returns:
            bool: true if storekeeper, otherwise false.
        """
        return self.role == "storekeeper"

    def is_customer(self):
        """Check if user is customer
        
        Returns:
            bool: true if customer, otherwise false.
        """
        return self.role == "customer"
