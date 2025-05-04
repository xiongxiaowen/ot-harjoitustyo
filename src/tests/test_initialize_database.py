import unittest
import sqlite3
from src.initialize_database import create_tables, initialize_database
from src.database_connection import get_database_connection
from unittest.mock import patch, MagicMock


class TestInitializeDatabase(unittest.TestCase):
    def setUp(self):
        #setup a database for testing
        self.connection =sqlite3.connect(":memory:")

    def test_create_tables(self):
        create_tables(self.connection)

        cursor = self.connection.cursor()

        #Check if "users" table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        self.assertIsNotNone(cursor.fetchone(), "Users table was not created.")

        # Check if 'transactions' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
        self.assertIsNotNone(cursor.fetchone(), "Transactions table was not created.")

    @patch("src.initialize_database.get_database_connection")
    def test_initialize_database(self, mock_get_db_connection):
        mock_conn = MagicMock() #create a mock DB
        mock_get_db_connection.return_value = mock_conn #return mock_conn mock DB 

        initialize_database()
        mock_get_db_connection.assert_called_once()
        mock_conn.cursor.assert_called()
        mock_conn.commit.assert_called()

 
if __name__ == "__main__":
    unittest.main()