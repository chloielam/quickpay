from .transactions_validators import validate_deposit_amount, validate_insufficient_funds
from .transactions_schemas import DepositCreate, DepositResponse, TransferCreate, TransferResponse
from app.transactions.transactions_repository import save_deposit, save_transfer
from app.users.users_repository import get_user_balance, get_user_by_id


def create_deposit(deposit_data: DepositCreate) -> DepositResponse:
    validate_deposit_amount(deposit_data.amount)
    return save_deposit(deposit_data)


def create_transfer(transfer_data: TransferCreate) -> TransferResponse:
    fee = round(transfer_data.amount * 0.01, 2)
    total_debit = transfer_data.amount + fee
    sender_balance = get_user_balance(transfer_data.sender_id)
    validate_insufficient_funds(sender_balance, total_debit)
    return save_transfer(transfer_data)
