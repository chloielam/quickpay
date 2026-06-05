from .transactions_validators import validate_deposit_amount, validate_insufficient_funds
from .transactions_schemas import DepositCreate, DepositResponse, TransferCreate, TransferResponse
from app.transactions.transactions_repository import save_deposit, save_transfer
from app.users.users_repository import get_user_balance, get_user_by_id


def create_deposit(deposit_data: DepositCreate) -> DepositResponse:
    validate_deposit_amount(deposit_data.amount)
    return save_deposit(deposit_data)


def create_transfer(transfer_data: TransferCreate) -> TransferResponse:
    total_amount = transfer_data.amount * 1.01  # Include 1% fee
    sender_balance = get_user_balance(transfer_data.sender_id)
    validate_insufficient_funds(sender_balance, total_amount)
    return save_transfer(transfer_data)
