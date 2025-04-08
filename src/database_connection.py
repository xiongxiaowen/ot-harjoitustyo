import os
import sqlite3

dirname = os.path.dirname(__file__)

#allow to create data folder if not exist
os.makedirs(os.path.dirname(os.path.join(dirname, "..", "data", "membership_card.db")), exist_ok=True) 

connection = sqlite3.connect(os.path.join(dirname, "..", "data", "membership_card.db"))
connection.row_factory=sqlite3.Row

def get_database_connection():
    return connection