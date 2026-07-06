from itertools import count
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import repositories as storage_repositories
from app.transactions.transactions_schemas import DepositCreate
from app.transactions.transactions_services import create_deposit
from app.users.users_schemas import UserCreate
from app.users.users_services import create_user


@pytest.fixture
def db_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "quickpay-test.db"
    monkeypatch.setenv("QUICKPAY_DB_PATH", str(path))
    monkeypatch.setattr(storage_repositories, "DATABASE_PATH", path)
    storage_repositories.init_db()
    return path


@pytest.fixture
def user_id_sequence() -> count:
    return count(start=1000)


@pytest.fixture
def client(db_path: Path) -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def create_user_payload(user_id_sequence: count):
    def _create_payload(*, age: int = 25, email: str | None = None, legal_name: str | None = None) -> dict:
        user_id = f"user-{next(user_id_sequence)}"
        return {
            "user_id": user_id,
            "legal_name": legal_name or f"User {user_id}",
            "email": email or f"user{user_id}@gmail.com",
            "age": age,
        }

    return _create_payload


@pytest.fixture
def create_api_user(client: TestClient, create_user_payload):
    def _create_user(*, age: int = 25, email: str | None = None, legal_name: str | None = None) -> dict:
        payload = create_user_payload(age=age, email=email, legal_name=legal_name)
        response = client.post("/users/create", json=payload)
        assert response.status_code == 201, response.json()
        return response.json()

    return _create_user


@pytest.fixture
def create_service_user(db_path: Path, create_user_payload):
    def _create_user(*, age: int = 25, email: str | None = None, legal_name: str | None = None):
        payload = create_user_payload(age=age, email=email, legal_name=legal_name)
        return create_user(UserCreate(**payload))

    return _create_user


@pytest.fixture
def seed_balance(db_path: Path):
    def _seed_balance(*, user_id: str, amount: float) -> None:
        create_deposit(DepositCreate(amount=amount, user_id=user_id))

    return _seed_balance
