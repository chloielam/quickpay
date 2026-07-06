import pytest

from app.transactions.transactions_schemas import DepositCreate, TransferCreate
from app.transactions.transactions_services import create_deposit, create_transfer
from app.users.users_repository import get_user_balance


def test_create_deposit_rejects_missing_user(db_path) -> None:
    with pytest.raises(ValueError, match="ERR_USER_NOT_FOUND"):
        create_deposit(DepositCreate(amount=100.0, user_id="missing-user"))


def test_create_deposit_updates_existing_balance(create_service_user) -> None:
    user = create_service_user()

    deposit = create_deposit(DepositCreate(amount=100.0, user_id=user.uid))

    assert deposit.amount == 100.0
    assert get_user_balance(user.uid) == 100.0


def test_create_transfer_rejects_non_positive_amount(create_service_user) -> None:
    sender = create_service_user(email="gtlam@mun.ca")
    receiver = create_service_user(email="yoopies.lam@gmail.com")

    with pytest.raises(ValueError, match="ERR_INVALID_TRANSFER_AMOUNT"):
        create_transfer(TransferCreate(amount=0.0, sender_id=sender.uid, receiver_id=receiver.uid))


def test_create_transfer_rejects_missing_sender(create_service_user) -> None:
    receiver = create_service_user(email="yoopies.lam@gmail.com")

    with pytest.raises(ValueError, match="ERR_USER_NOT_FOUND"):
        create_transfer(TransferCreate(amount=10.0, sender_id="missing-user", receiver_id=receiver.uid))


def test_create_transfer_rejects_missing_receiver(create_service_user, seed_balance) -> None:
    sender = create_service_user(email="gtlam@mun.ca")
    seed_balance(user_id=sender.uid, amount=100.0)

    with pytest.raises(ValueError, match="ERR_USER_NOT_FOUND"):
        create_transfer(TransferCreate(amount=10.0, sender_id=sender.uid, receiver_id="missing-user"))


def test_create_transfer_rejects_insufficient_funds(create_service_user, seed_balance) -> None:
    sender = create_service_user(email="gtlam@mun.ca")
    receiver = create_service_user(email="yoopies.lam@gmail.com")
    seed_balance(user_id=sender.uid, amount=10.0)

    with pytest.raises(ValueError, match="ERR_INSUFFICIENT_FUNDS"):
        create_transfer(TransferCreate(amount=10.0, sender_id=sender.uid, receiver_id=receiver.uid))


def test_create_transfer_debits_sender_and_credits_receiver(create_service_user, seed_balance) -> None:
    sender = create_service_user(email="gtlam@mun.ca")
    receiver = create_service_user(email="yoopies.lam@gmail.com")
    seed_balance(user_id=sender.uid, amount=101.0)

    transfer = create_transfer(TransferCreate(amount=100.0, sender_id=sender.uid, receiver_id=receiver.uid))

    assert transfer.amount == 100.0
    assert get_user_balance(sender.uid) == 0.0
    assert get_user_balance(receiver.uid) == 100.0
