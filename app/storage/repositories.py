import os
import sqlite3
from pathlib import Path


def get_database_path() -> Path:
    env_path = os.getenv("QUICKPAY_DB_PATH")
    if env_path:
        return Path(env_path)
    return Path(__file__).resolve().parents[2] / "quickpay.db"


DATABASE_PATH = get_database_path()


def _has_legacy_numeric_id_schema(conn: sqlite3.Connection) -> bool:
    expected_types = {
        ("users", "uid"): "TEXT",
        ("deposits", "user_id"): "TEXT",
        ("transfers", "sender_id"): "TEXT",
        ("transfers", "receiver_id"): "TEXT",
    }
    for (table, column), expected_type in expected_types.items():
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
        if not rows:
            continue
        column_info = next((row for row in rows if row[1] == column), None)
        if not column_info or column_info[2].upper() != expected_type:
            return True
    return False


def _reset_legacy_schema(conn: sqlite3.Connection) -> None:
    conn.execute("DROP TABLE IF EXISTS transfers")
    conn.execute("DROP TABLE IF EXISTS deposits")
    conn.execute("DROP TABLE IF EXISTS users")


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        if _has_legacy_numeric_id_schema(conn):
            _reset_legacy_schema(conn)

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT PRIMARY KEY,
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
                user_id TEXT NOT NULL,
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
                sender_id TEXT NOT NULL,
                receiver_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(sender_id) REFERENCES users(uid),
                FOREIGN KEY(receiver_id) REFERENCES users(uid)
            )
            """
        )
        conn.commit()
