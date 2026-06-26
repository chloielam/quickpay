from ..core.errors import ERR_DEPOSIT_LIMIT, ERR_INSUFFICIENT_FUNDS, ERR_INVALID_TRANSFER_AMOUNT


def validate_deposit_amount(amount: float) -> bool:
    if amount < 5 or amount > 5000:
        raise ValueError(ERR_DEPOSIT_LIMIT)
    return True

def validate_insufficient_funds(balance: float, amount: float) -> bool:
    if balance < amount:
        raise ValueError(ERR_INSUFFICIENT_FUNDS)
    return True


def validate_transfer_amount(amount: float) -> bool:
    if amount <= 0:
        raise ValueError(ERR_INVALID_TRANSFER_AMOUNT)
    return True

