import unittest
import sqlite3
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.database_connection import get_database_connection


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        #setup a database for testing
        self.connection =sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.create_tables()
        self.repo = UserRepository()
        self.repo._connection = self.connection

        self.connection.execute("INSERT INTO users (username, password, role, balance) VALUES (?, ?, ?, ?)",
                                ("test_user2", "password2", "customer", 100.0))
        self.connection.commit()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NUll,
                role TEXT CHECK (role IN ('customer', 'storekeeper')) NOT NULL,
                balance REAL DEFAULT 0.00
            )
        """)
        cursor.execute("""
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT CHECK(payment_method IN ('cash', 'card')) NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        self.connection.commit()

    def test_user_repository_setup_ok(self):
        #user_repository successfully created
        self.assertNotEqual(self.repo, None) 

    
    def test_find_user_by_username(self):
        user = self.repo.find_user_by_username("test_user2")
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "test_user2")
        self.assertEqual(user.password, "password2")
        self.assertEqual(user.role, "customer")
        self.assertEqual(user.balance, 100.0)

        #for non-existing user
        user_not_found = self.repo.find_user_by_username("non_existent_user")
        self.assertIsNone(user_not_found)

    def test_create_user(self):
        # create user successfully
        new_user = User("testUser3", "newpassword3", "customer", 50.0)
        #verify the test user no exist before creating user
        self.assertIsNone(self.repo.find_user_by_username("testUser3"))
        result =self.repo.create_user(new_user)
        self.assertTrue(result)

        # Verify that the new user is created in the database
        created_user = self.repo.find_user_by_username("testUser3")
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, new_user.username)

        #Try to create a user with the same username
        duplicate_user = User("testUser3", "another_password", "customer", 75.0)
        result = self.repo.create_user(duplicate_user)
        self.assertFalse(result)

    def test_delete_user(self):
        self.repo.delete_user("test_user2")
        user = self.repo.find_user_by_username("test_user2")
        self.assertIsNone(user)

    def test_update_password(self):
        user = self.repo.find_user_by_username("test_user2")
        self.repo.update_password("test_user2", "password_updated")
        cursor = self.connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", ("test_user2",))
        self.assertEqual(cursor.fetchone()[0], "password_updated")

    def test_get_balance(self):
        user = self.repo.find_user_by_username("test_user2")
        self.repo.get_balance(user.username)
        self.assertEqual(user.balance, 100.0)

    def test_update_balance(self):
        # Test deposit
        self.repo.update_balance("test_user2", 50.0)
        self.assertEqual(self.repo.get_balance("test_user2"), 150.0)     
        # Test withdrawal
        self.repo.update_balance("test_user2", -30.0)
        self.assertEqual(self.repo.get_balance("test_user2"), 120.0)

    def test_get_all_customers(self):
        self.connection.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
            ("admin_user", "adminpass", "storekeeper", 500.0))
        customers = self.repo.get_all_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].username, "test_user2")
        self.assertEqual(customers[0].role, "customer")
 
if __name__ == "__main__":
    unittest.main()