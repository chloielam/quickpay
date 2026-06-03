from typing import Optional

from app.users.users_schemas import UserCreate, UserResponse
from app.storage.repositories import get_connection

def save_user(user_data: UserCreate) -> UserResponse:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (legal_name, email, age, balance) VALUES (?, ?, ?, ?)",
            (user_data.legal_name, user_data.email, user_data.age, 0.0)
        )
        uid = cursor.lastrowid
        conn.commit()
        return UserResponse(uid=uid, legal_name=user_data.legal_name, email=user_data.email, age=user_data.age, balance=0.0)

def get_user_by_id(uid: int) -> Optional[UserResponse]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT uid, legal_name, email, age, balance FROM users WHERE uid = ?", (uid,))
        row = cursor.fetchone()
        return UserResponse(uid=row[0], legal_name=row[1], email=row[2], age=row[3], balance=row[4]) if row else None


def get_user_by_email(email: str) -> Optional[UserResponse]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT uid, legal_name, email, age, balance FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return UserResponse(uid=row[0], legal_name=row[1], email=row[2], age=row[3], balance=row[4]) if row else None


def get_user_balance(user_id: int) -> float:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE uid = ?", (user_id,))
        row = cursor.fetchone()
        return float(row[0]) if row else 0.0
