from src.repositories.user_repository import UserRepository
from src.models.user import User

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, username, password):
        #allow log in
        user = self.user_repository.find_user_by_username(username)
        if not user or user.password != password:
            raise InvalidCredentialsError("Invalid username or password")
        if user and user.password == password:
            return user
        return None

    def create_user(self, username, password):
        #allow create new user, if no existing user name
        existing_user = self.user_repository.find_by_username(username)
        if existing_user:
            raise UsernameExistsError(f"Username {username} already exists")
        user = self.user_repository.create_user(User(username, password))
        return user

    def delete_user(self, username):
        #Delete user account
        user = self.user_repository.find_user_by_username(username)
        if user:
            return self.user_repository.remove_user(user)
        return False
    
    def logout(self):
        #Logout current user
        pass