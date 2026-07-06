import pytest

from app.transactions.transactions_validators import (
    validate_deposit_amount,
    validate_insufficient_funds,
    validate_transfer_amount,
)


@pytest.mark.parametrize("amount", [4.99, 5000.01])
def test_validate_deposit_amount_rejects_out_of_range_values(amount: float) -> None:
    with pytest.raises(ValueError, match="ERR_DEPOSIT_LIMIT"):
        validate_deposit_amount(amount)


@pytest.mark.parametrize("amount", [5.0, 5000.0])
def test_validate_deposit_amount_accepts_boundaries(amount: float) -> None:
    assert validate_deposit_amount(amount) is True


@pytest.mark.parametrize("amount", [0.0, -1.0])
def test_validate_transfer_amount_rejects_non_positive_values(amount: float) -> None:
    with pytest.raises(ValueError, match="ERR_INVALID_TRANSFER_AMOUNT"):
        validate_transfer_amount(amount)


def test_validate_transfer_amount_accepts_positive_value() -> None:
    assert validate_transfer_amount(10.0) is True


def test_validate_insufficient_funds_rejects_lower_balance() -> None:
    with pytest.raises(ValueError, match="ERR_INSUFFICIENT_FUNDS"):
        validate_insufficient_funds(9.99, 10.0)


@pytest.mark.parametrize(("balance", "amount"), [(10.0, 10.0), (20.0, 10.0)])
def test_validate_insufficient_funds_accepts_equal_or_greater_balance(balance: float, amount: float) -> None:
    assert validate_insufficient_funds(balance, amount) is True