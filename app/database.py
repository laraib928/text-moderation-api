import sqlite3
from datetime import datetime

# Initialize and connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect("moderation.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Create the table (run once at startup)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS moderation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            text TEXT NOT NULL,
            decision TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
