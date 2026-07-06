import pytest
from fastapi.testclient import TestClient

from app.transactions import transactions_routes

def test_deposit_route_returns_404_for_missing_user(client: TestClient) -> None:
    response = client.post("/transactions/deposit", json={"amount": 100.0, "user_id": 9999})

    assert response.status_code == 404
    assert response.json() == {"detail": "ERR_USER_NOT_FOUND"}


@pytest.mark.parametrize("amount", [0.0, -5.0])
def test_transfer_route_returns_400_for_invalid_amount(client: TestClient, create_api_user, amount: float) -> None:
    sender = create_api_user(email="gtlam@mun.ca")
    receiver = create_api_user(email="yoopies.lam@gmail.com")

    response = client.post(
        "/transactions/transfer",
        json={"amount": amount, "sender_id": sender["uid"], "receiver_id": receiver["uid"]},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "ERR_INVALID_TRANSFER_AMOUNT"}


def test_transfer_route_returns_404_for_missing_user(client: TestClient, create_api_user) -> None:
    sender = create_api_user(email="gtlam@mun.ca")

    response = client.post(
        "/transactions/transfer", 
        json={"amount": 10.0, "sender_id": sender["uid"], "receiver_id": 9999},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "ERR_USER_NOT_FOUND"}


def test_transfer_route_returns_400_for_insufficient_funds(client: TestClient, create_api_user) -> None:
    sender = create_api_user(email="gtlam@mun.ca")
    receiver = create_api_user(email="yoopies.lam@gmail.com")

    response = client.post(
        "/transactions/transfer",
        json={"amount": 10.0, "sender_id": sender["uid"], "receiver_id": receiver["uid"]},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "ERR_INSUFFICIENT_FUNDS"}


def test_get_deposits_returns_saved_deposits(client: TestClient, create_api_user) -> None:
    user = create_api_user()
    client.post("/transactions/deposit", json={"amount": 25.0, "user_id": user["uid"]})

    response = client.get("/transactions/deposits")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["amount"] == 25.0


def test_get_transfers_returns_saved_transfers(client: TestClient, create_api_user) -> None:
    sender = create_api_user(email="gtlam@mun.ca")
    receiver = create_api_user(email="yoopies.lam@gmail.com")
    client.post("/transactions/deposit", json={"amount": 101.0, "user_id": sender["uid"]})
    client.post(
        "/transactions/transfer",
        json={"amount": 100.0, "sender_id": sender["uid"], "receiver_id": receiver["uid"]},
    )

    response = client.get("/transactions/transfers")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["amount"] == 100.0

def test_deposit_route_returns_generic_400_for_unknown_value_error(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_create_deposit(_):
        raise ValueError("UNEXPECTED_DEPOSIT_ERROR")

    monkeypatch.setattr(transactions_routes, "create_deposit", fake_create_deposit)

    response = client.post("/transactions/deposit", json={"amount": 100.0, "user_id": 1000})

    assert response.status_code == 400
    assert response.json() == {"detail": "UNEXPECTED_DEPOSIT_ERROR"}


def test_transfer_route_returns_generic_400_for_unknown_value_error(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_create_transfer(_):
        raise ValueError("UNEXPECTED_TRANSFER_ERROR")

    monkeypatch.setattr(transactions_routes, "create_transfer", fake_create_transfer)

    response = client.post(
        "/transactions/transfer",
        json={"amount": 10.0, "sender_id": 1000, "receiver_id": 1001},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "UNEXPECTED_TRANSFER_ERROR"}