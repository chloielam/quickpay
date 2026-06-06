from datetime import datetime

from app.transactions.transactions_schemas import DepositCreate, DepositResponse, TransferCreate, TransferResponse
from app.storage.repositories import get_connection


def save_deposit(deposit_data: DepositCreate) -> DepositResponse:
    timestamp = datetime.utcnow().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO deposits (amount, user_id, timestamp) VALUES (?, ?, ?)",
            (deposit_data.amount, deposit_data.user_id, timestamp)
        )
        tid = cursor.lastrowid
        conn.execute(
            "UPDATE users SET balance = balance + ? WHERE uid = ?",
            (deposit_data.amount, deposit_data.user_id),
        )
        conn.commit()
        return DepositResponse(tid=tid, amount=deposit_data.amount, user_id=deposit_data.user_id, timestamp=timestamp)
    
def save_transfer(transfer_data: TransferCreate) -> TransferResponse:
    timestamp = datetime.utcnow().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transfers (amount, sender_id, receiver_id, timestamp) VALUES (?, ?, ?, ?)",
            (transfer_data.amount, transfer_data.sender_id, transfer_data.receiver_id, timestamp)
        )
        tid = cursor.lastrowid
        fee = round(transfer_data.amount * 0.01, 2)
        total_debit = transfer_data.amount + fee
        conn.execute(
            "UPDATE users SET balance = balance - ? WHERE uid = ?",
            (total_debit, transfer_data.sender_id),
        )
        conn.execute(
            "UPDATE users SET balance = balance + ? WHERE uid = ?",
            (transfer_data.amount, transfer_data.receiver_id),
        )
        conn.commit()
        return TransferResponse(tid=tid, amount=transfer_data.amount, sender_id=transfer_data.sender_id, receiver_id=transfer_data.receiver_id, timestamp=timestamp)