import pytest

from app.users.users_validators import validate_age, validate_email


def test_validate_age_rejects_under_18() -> None:
    with pytest.raises(ValueError, match="ERR_AGE_RESTRICTED"):
        validate_age(17)


def test_validate_age_accepts_18() -> None:
    assert validate_age(18) is True


def test_validate_email_accepts_valid_email() -> None:
    assert validate_email("gtlam@hcmut.edu.vn") is True


@pytest.mark.parametrize("email", ["gtlam.com", "gtlam@@mun.ca", "gtlam@munca"])
def test_validate_email_rejects_invalid_inputs(email: str) -> None:
    with pytest.raises(ValueError, match="ERR_INVALID_EMAIL"):
        validate_email(email)



