import os
import sqlite3
from pathlib import Path


def get_database_path() -> Path:
    env_path = os.getenv("QUICKPAY_DB_PATH")
    if env_path:
        return Path(env_path)
    return Path(__file__).resolve().parents[2] / "quickpay.db"


DATABASE_PATH = get_database_path()

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


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
