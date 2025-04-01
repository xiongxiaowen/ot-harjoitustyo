from src.models.user import User

class UserRepository: 
    def __init_(self):
        self.users = {}

    #find a user by username
    def find_user_by_username(self, username) -> User:
        return self.users.get(username)

    #create a new user
    def create_user(self, user: User):
        if user.username in self.users: 
            return "username already existing"
        self.users[user.username] = user
        return True

    #allow to remove a user
    def remove_user(self, user: User):
        if user.username in self.users:
            del self.users[user.username]
            return True
        return False