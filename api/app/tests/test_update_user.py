from fastapi.testclient import TestClient


def test_update_user(client: TestClient):
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
    user_id = created_user["id"]

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
    assert updated_user["is_active"] == user_data["is_active"]
    assert updated_user["is_superuser"] == user_data["is_superuser"]
