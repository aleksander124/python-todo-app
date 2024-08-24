from fastapi.testclient import TestClient


def create_user(client: TestClient):
    user_data = {
        "username": "user-to-delete",
        "email": "user@test.com",
        "password": "testpassword",
        "is_active": True,
        "is_superuser": False
    }

    response = client.post("/auth/create-user/", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    return created_user["id"], user_data


def test_delete_user(client: TestClient):
    user_id, _ = create_user(client)

    response = client.delete(f"/auth/users/{user_id}/")
    assert response.status_code == 200


def test_delete_user_invalid_user(client: TestClient):
    user_id, _ = create_user(client)

    invalid_user_id = 99
    response = client.delete(f"/auth/users/{invalid_user_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
