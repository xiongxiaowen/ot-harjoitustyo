import sqlite3
import os
from src.database_connection import get_database_connection

DB_FILE = os.path.join(os.path.dirname(__file__), "membership_card.db")

def create_tables(connection):
        """Create databased tables. Two tables needed, one for user data, one for payment transactions.
        set up foreign key relationship between the transactions and users tables.
        """
        cursor = connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;") 

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK (role IN ('customer', 'storekeeper')) NOT NULL,
            balance REAL DEFAULT 0.00
            );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT CHECK(payment_method IN ('cash', 'card')) NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """)

        connection.commit()
        #use this line to verify if creation ok: print("Database and tables created successfully.")


def initialize_database():

    connection = get_database_connection()
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()