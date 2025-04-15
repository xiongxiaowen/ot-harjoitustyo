from src.repositories.user_repository import UserRepository
from src.models.user import User

class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def login(self, username, password):
        user = self.user_repository.find_user_by_username(username)
        return user if user and user.password == password else None

    def register(self, username, password, role):
        user = User(username=username, password=password, role=role)
        return self.user_repository.create_user(user)

    def delete_account(self, username):
        self.user_repository.delete_user(username)

    def change_password(self, username, new_password):
        self.user_repository.update_password(username, new_password)

    def get_balance(self, username):
        return self.user_repository.get_balance(username)
    
    def logout(self):
        #Logout current user
        self.current_user = None

