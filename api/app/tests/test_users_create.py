from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    user_data = {
        "username": "testuser",
        "email": "test@test.com",
        "password": "test",
        "is_active": True,
        "is_superuser": False
    }

    response = client.post("/auth/create-user/", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["is_active"] == user_data["is_active"]
    assert response_data["is_superuser"] == user_data["is_superuser"]


def test_create_duplicated_user_username(client: TestClient):
    user_data = {
        "username": "testuser",
        "email": "test2@test.com",
        "password": "test",
        "is_active": True,
        "is_superuser": False
    }

    response = client.post("/auth/create-user/", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


def test_create_duplicated_user_email(client: TestClient):
    # First, create a user with a specific email
    user_data = {
        "username": "testuser2",
        "email": "test@test.com",
        "password": "test",
        "is_active": True,
        "is_superuser": False
    }

    response = client.post("/auth/create-user/", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_create_user_invalid_email(client: TestClient):
    user_data = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "test",
        "is_active": True,
        "is_superuser": False
    }

    response = client.post("/auth/create-user/", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email address"}
