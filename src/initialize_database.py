import sqlite3
import os
from database_connection import get_database_connection

DB_FILE = os.path.join(os.path.dirname(__file__), "membership_card.db")
#Two tables will be needed, one for user data, one for payment transactions

def create_tables(connection):
        cursor = connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;") #fogeign key needed between 2 tables

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NUll,
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
        print("Database and tables created successfully.")


def initialize_database():

    connection = get_database_connection()
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()