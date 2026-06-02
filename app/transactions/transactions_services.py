from .transactions_validators import validate_deposit_amount, validate_insufficient_funds
from .transactions_schemas import DepositCreate, DepositResponse, TransferCreate, TransferResponse

def create_deposit(deposit_data: DepositCreate) -> DepositResponse:
    validate_deposit_amount(deposit_data.amount)
    return DepositResponse(tid=1, amount=deposit_data.amount, user_id=deposit_data.user_id, timestamp="2024-01-01T00:00:00Z")

def create_transfer(transfer_data: TransferCreate, sender_balance: float) -> TransferResponse:
    validate_deposit_amount(transfer_data.amount)
    validate_insufficient_funds(sender_balance, transfer_data.amount)
    return TransferResponse(tid=1, amount=transfer_data.amount, sender_id=transfer_data.sender_id, receiver_id=transfer_data.receiver_id, timestamp="2024-01-01T00:00:00Z")
