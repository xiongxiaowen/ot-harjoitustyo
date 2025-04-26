import sqlite3
from src.models.transaction import Transaction
from src.database_connection import get_database_connection

class TransactionRepository:
    def __init__(self):
        self._connection = get_database_connection()

    def save_transaction(self, transaction: Transaction):
        """Save new transaction to database."""
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO transactions (user_id, amount, payment_method, date)
            VALUES (?, ?, ?, ?)
        """, (transaction.user_id, transaction.amount, transaction.payment_method, transaction.date))
        self._connection.commit()


    def get_transactions_by_username(self, username):
        """Get all transactions based on specific username."""
        cursor = self._connection.cursor()
        cursor.execute("SELECT t.date, t.amount, t.payment_method FROM transactions t JOIN users u ON t.user_id = u.id WHERE u.username = ? ORDER BY t.date DESC", (username,))
        return [{"date": row[0], "amount": row[1], "method": row[2]} for row in cursor.fetchall()]


    def get_all_transactions(self):
        """Get for admin fetch all transaction histories.

        Returns:
            list: a dictionary with transaction detials. 
        """
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT transactions.date, transactions.amount, transactions.payment_method, transactions.user_id, users.username
            FROM transactions
            JOIN users ON transactions.user_id = users.id
            ORDER BY transactions.date DESC;
        """)
        rows = cursor.fetchall()
        transactions = []
        for row in rows:
            transactions.append({
                "date": row["date"],
                "amount": row["amount"],
                "payment_method": row["payment_method"],
                "user_id": row["user_id"],
                "username": row["username"]
            })
        return transactions

    def get_total_revenue(self):
        """Get sum of all card and cash payments."""
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT SUM(amount) as total FROM transactions
            WHERE payment_method IN ('card', 'cash');
        """)
        row = cursor.fetchone()
        return row["total"] if row["total"] else 0.0

    def get_cash_register_balance(self):
        """Get Sum of all cash payments"""
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT SUM(amount) as total FROM transactions
            WHERE payment_method = 'cash';
        """)
        row = cursor.fetchone()
        return row["total"] if row["total"] else 0.0



