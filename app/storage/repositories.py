import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parents[2] / "quickpay.db"

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                legal_name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0
            )
            """
        )
 
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS deposits (
                tid INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                user_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(uid)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transfers (
                tid INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(sender_id) REFERENCES users(uid),
                FOREIGN KEY(receiver_id) REFERENCES users(uid)
            )
            """
        )
        conn.commit()


