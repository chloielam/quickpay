import pytest
from fastapi.testclient import TestClient

from app.users import users_routes


def test_get_users_returns_created_users(client: TestClient, create_api_user) -> None:
    first_user = create_api_user(email="gtlam@mun.ca")
    second_user = create_api_user(email="truc.lamg@gmail.com")

    response = client.get("/users/")

    assert response.status_code == 200
    assert response.json() == [first_user, second_user]


def test_get_user_balance_returns_404_for_missing_user(client: TestClient) -> None:
    response = client.get("/users/9999/balance")

    assert response.status_code == 404
    assert response.json() == {"detail": "ERR_USER_NOT_FOUND"}


def test_get_user_balance_returns_existing_user_balance(client: TestClient, create_api_user) -> None:
    user = create_api_user()

    response = client.get(f"/users/{user['uid']}/balance")

    assert response.status_code == 200
    assert response.json() == {"uid": user["uid"], "balance": 0.0}


def test_health_route_returns_running_message(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "QuickPay is running!"}

def test_user_create_route_returns_generic_400_for_unknown_value_error(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_create_user(_):
        raise ValueError("UNEXPECTED_USER_ERROR")

    monkeypatch.setattr(users_routes, "create_user", fake_create_user)

    response = client.post(
        "/users/create",
        json={"user_id": 9991, "legal_name": "Route User", "email": "route@example.com", "age": 24},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "UNEXPECTED_USER_ERROR"}


def test_user_balance_route_returns_generic_400_for_unknown_value_error(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get_user_balance_info(_):
        raise ValueError("UNEXPECTED_BALANCE_ERROR")

    monkeypatch.setattr(users_routes, "get_user_balance_info", fake_get_user_balance_info)

    response = client.get("/users/1000/balance")

    assert response.status_code == 400
    assert response.json() == {"detail": "UNEXPECTED_BALANCE_ERROR"}




