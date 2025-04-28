import sqlite3
from src.models.user import User
from src.database_connection import get_database_connection

class UserRepository:
    """_summary_
    """
    def __init__(self):
        self._connection = get_database_connection()

    #find a user by username
    def find_user_by_username(self, username):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return User(*row)
        return None

    #create a new user
    def create_user(self, user):
        try:
            cursor = self._connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role, balance) VALUES (?, ?, ?, ?)",
                (user.username, user.password, user.role, user.balance)
                )
            self._connection.commit()
            return True
        except sqlite3.IntegrityError:
            self._connection.rollback()
            return False

    #allow to remove a user
    def delete_user(self, username):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self._connection.commit()

    #update password
    def update_password(self, username, new_password):
        cursor = self._connection.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        self._connection.commit()

    def get_balance(self, username):
        cursor = self._connection.cursor()
        cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row[0] if row else 0.0

    def update_balance(self, username, amount):
        cursor = self._connection.cursor()
        cursor.execute("UPDATE users SET balance = balance + ? WHERE username = ?",
                       (amount, username)
                       )
        self._connection.commit()
        return True

    def get_all_customers(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT username, balance FROM users WHERE role='customer'")
        rows = cursor.fetchall()
        return [User(username=row[0], password="", role="customer", balance=row[1]) for row in rows]