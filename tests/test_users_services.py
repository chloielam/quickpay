import pytest

from app.storage.repositories import get_database_path
from app.users.users_repository import get_user_by_email
from app.users.users_schemas import UserCreate
from app.users.users_services import create_user, get_user_balance_info


def test_create_user_persists_valid_user(db_path, create_user_payload) -> None:
    user = create_user(UserCreate(**create_user_payload(age=25, email="valid@example.com")))

    assert user.uid >= 1000
    assert user.balance == 0.0


def test_create_user_rejects_duplicate_user_id(db_path) -> None:
    payload = {
        "user_id": 2001,
        "legal_name": "Original User",
        "email": "original@example.com",
        "age": 25,
    }
    create_user(UserCreate(**payload))

    with pytest.raises(ValueError, match="ERR_DUPLICATE_USER_ID"):
        create_user(UserCreate(**{**payload, "email": "duplicate@example.com"}))


def test_get_user_by_email_returns_created_user(create_service_user) -> None:
    user = create_service_user(email="lookup@example.com")

    lookup = get_user_by_email("lookup@example.com")

    assert lookup is not None
    assert lookup.uid == user.uid


def test_get_database_path_uses_environment_override(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    custom_path = tmp_path / "custom.db"
    monkeypatch.setenv("QUICKPAY_DB_PATH", str(custom_path))

    assert get_database_path() == custom_path


def test_get_user_balance_info_returns_existing_balance(create_service_user) -> None:
    user = create_service_user()

    balance = get_user_balance_info(user.uid)

    assert balance.uid == user.uid
    assert balance.balance == 0.0


def test_get_user_balance_info_rejects_missing_user(db_path) -> None:
    with pytest.raises(ValueError, match="ERR_USER_NOT_FOUND"):
        get_user_balance_info(9999)



