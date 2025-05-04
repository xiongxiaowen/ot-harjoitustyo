import os
import sqlite3

dirname = os.path.dirname(__file__)

"""allow to create data folder if not exist"""
db_path = os.path.abspath(os.path.join(dirname, "..", "data", "membership_card.db"))
os.makedirs(os.path.dirname(db_path), exist_ok=True)


connection = sqlite3.connect(db_path, check_same_thread=False)
connection.row_factory=sqlite3.Row

def get_database_connection():
    return connection