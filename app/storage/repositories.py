import sqlite3
from pathlib import Path

from app.users.users_schemas import UserCreate, UserResponse
from app.transactions.transactions_schemas import DepositCreate, DepositResponse, TransferCreate, TransferResponse


DATABASE_PATH = Path(__file__).resolve().parents[2] / "quickpay.db"

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def _ensure_user_balance_column(conn):
    cursor = conn.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    if "balance" not in columns:
        conn.execute("ALTER TABLE users ADD COLUMN balance REAL NOT NULL DEFAULT 0.0")


def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                legal_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0
            )
            """
        )
        _ensure_user_balance_column(conn)
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


