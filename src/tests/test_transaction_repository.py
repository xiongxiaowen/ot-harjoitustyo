import unittest
import sqlite3
from src.repositories.transaction_repository import TransactionRepository
from src.models.transaction import Transaction
from src.database_connection import get_database_connection
from datetime import datetime

class TestTransactionRepository(unittest.TestCase):
    def setUp(self):
        #setup a database
        self.connection =sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.create_tables()
        self.repo = TransactionRepository()
        self.repo._connection = self.connection

        self.connection.execute("INSERT INTO users (username, password, role, balance) VALUES (?, ?, ?, ?)",
                                ("test_user1", "password1", "customer", 50.0))
        self.connection.commit()
        self.user_id = self.connection.execute("SELECT id FROM users WHERE username = ?", ("test_user1",)).fetchone()["id"]

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

    def test_transaction_repository_setup_ok(self):
        #transaction_repository successfully created
        self.assertNotEqual(self.repo, None) 

    
    def test_save_transaction_and_fetch(self):
        #test save_transaction ok, verifies transactions are appended
        tx = Transaction(self.user_id, 100.0, "card", datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.repo.save_transaction(tx)

        all_tx = self.repo.get_all_transactions()
        self.assertEqual(len(all_tx), 1)
        self.assertEqual(all_tx[0]["amount"], 100.0)

    def test_get_transactions_by_username(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        tx = Transaction(self.user_id, 25.0, "cash", now)
        self.repo.save_transaction(tx)

        result = self.repo.get_transactions_by_username("test_user1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["amount"], 25.0)
        self.assertEqual(result[0]["method"], "cash")


    def test_get_total_revenue(self):
        self.repo.save_transaction(Transaction(self.user_id, 50.0, "cash", datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.repo.save_transaction(Transaction(self.user_id, 20.0, "cash", datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.repo.save_transaction(Transaction(self.user_id, 10.0, "cash", datetime.now().strftime("%Y-%m-%d %H:%M")))

        total_revenue = self.repo.get_total_revenue()
        self.assertEqual(total_revenue, 80.0)

    def test_get_cash_register_balance(self):
        #card payment not included in cash register
        self.repo.save_transaction(Transaction(self.user_id, 30.0, "cash", datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.repo.save_transaction(Transaction(self.user_id, 20.0, "card", datetime.now().strftime("%Y-%m-%d %H:%M")))

        cash_balance = self.repo.get_cash_register_balance()
        self.assertEqual(cash_balance, 30.0)

if __name__ == "__main__":
    unittest.main()