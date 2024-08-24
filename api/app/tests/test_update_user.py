from fastapi.testclient import TestClient


def create_user(client: TestClient):
    user_data = {
        "username": "originaluser",
        "email": "original@test.com",
        "password": "testpassword",
        "is_active": True,
        "is_superuser": False
    }

    response = client.post("/auth/create-user/", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    return created_user["id"], user_data


def test_update_user(client: TestClient):
    user_id, original_user_data = create_user(client)

    update_data = {
        "username": "updateduser",
        "email": "updated@test.com",
    }

    response = client.put(f"/auth/users/{user_id}/", json=update_data)
    assert response.status_code == 200

    updated_user = response.json()

    assert updated_user["id"] == user_id
    assert updated_user["username"] == update_data["username"]
    assert updated_user["email"] == update_data["email"]
    assert updated_user["is_active"] == original_user_data["is_active"]
    assert updated_user["is_superuser"] == original_user_data["is_superuser"]


def test_update_user_invalid_email(client: TestClient):
    user_id, original_user_data = create_user(client)

    update_data = {
        "username": "updateduser",
        "email": "invalidemail",
    }

    response = client.put(f"/auth/users/{user_id}/", json=update_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email address"}


def test_update_user_not_exists(client: TestClient):
    update_data = {
        "username": "originaluser",
        "email": "original@test.com",
    }

    invalid_user_id = 99
    response = client.put(f"/auth/users/{invalid_user_id}/", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
