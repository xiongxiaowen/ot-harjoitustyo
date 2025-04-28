import unittest
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.services.user_service import UserService
from unittest.mock import Mock, patch

class TestUserService(unittest.TestCase):
    def setUp(self):
        #setup mock repository
        self.mock_repo = Mock()
        self.service = UserService(user_repository=self.mock_repo)
        #setup test user        
        self.test_user = User(
            user_id=1,
            username="test_user",
            password="correct_pass",
            role="customer",
            balance=100.0
        )

    def test_login_ok(self):
        self.mock_repo.find_user_by_username.return_value = self.test_user
        result = self.service.login("test_user", "correct_pass")
        self.assertEqual(result, self.test_user)
 
    def test_login_wrong_password(self):
        self.mock_repo.find_user_by_username.return_value = self.test_user
        result = self.service.login("test_user", "wrong_pass")
        self.assertIsNone(result)

    def test_failed_login_not_existing(self):
        #Should return None when user doesn't exist
        self.mock_repo.find_user_by_username.return_value = None
        result = self.service.login("unknown", "none")
        self.assertIsNone(result)

    def test_username_empty(self):
        #edge case: username field empty
        result = self.service.login(" ", "empty")
        self.assertIsNone(result)

    def test_successful_registration(self):
        #successfully register new user
        self.mock_repo.create_user.return_value = True
        
        result = self.service.register("new_user", "new_pass", "customer")
        self.assertTrue(result)
        self.mock_repo.create_user.assert_called_once()
        
        # Verify created user has correct attributes
        created_user = self.mock_repo.create_user.call_args[0][0]
        self.assertEqual(created_user.username, "new_user")
        self.assertEqual(created_user.password, "new_pass")
        self.assertEqual(created_user.role, "customer")

    def test_failed_registration(self):
        #return False when registration fails
        self.mock_repo.create_user.return_value = False
        result = self.service.register("existing_user", "fail", "customer")
        self.assertFalse(result)

    def test_delete_account(self):
        self.service.delete_account("test_user")
        self.mock_repo.delete_user.assert_called_once_with("test_user")

    def test_change_password(self):
        #update password in repository
        self.service.change_password("test_user", "new_secure_pass")
        self.mock_repo.update_password.assert_called_once_with("test_user", "new_secure_pass")

    def test_get_balance(self):
        #return balance from repository
        self.mock_repo.get_balance.return_value = 100.0
        balance = self.service.get_balance("test_user")
        self.assertEqual(balance, 100.0)
        self.mock_repo.get_balance.assert_called_once_with("test_user")

    def test_logout(self):
        self.service.current_user = self.test_user
        self.service.logout()
        self.assertIsNone(self.service.current_user)
        

if __name__ == "__main__":
    unittest.main()