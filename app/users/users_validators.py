from ..core.errors import ERR_AGE_RESTRICTED, ERR_INVALID_EMAIL

def validate_age(age: int) -> bool:
    if age < 18:
        raise ValueError(ERR_AGE_RESTRICTED)
    return True

def validate_email(email: str) -> bool:
    if email.count("@") != 1:
        raise ValueError(ERR_INVALID_EMAIL)
    if email.split("@")[1].count(".") < 1:
        raise ValueError(ERR_INVALID_EMAIL)
    return True

