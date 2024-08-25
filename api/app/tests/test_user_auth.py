from fastapi.testclient import TestClient


def create_user(client: TestClient):
    user_data = {
        "username": "auth-user",
        "email": "auth-user@test.com",
        "password": "testpassword",
        "is_active": True,
        "is_superuser": True
    }

    response = client.post("/auth/create-user/", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    return created_user["id"], user_data


def get_access_token(client: TestClient) -> str:
    token_data = {
        "grant_type": "password",
        "username": "auth-user",
        "password": "testpassword",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = client.post("/auth/token", data=token_data, headers=headers)
    assert response.status_code == 200
    created_token = response.json()
    assert "access_token" in created_token
    return created_token["access_token"]


def get_user_info(client: TestClient, access_token: str):
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json"
    }

    response = client.get("/auth/users/me/", headers=auth_headers)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["username"] == "auth-user"


def get_access_token_invalid_user(client: TestClient):
    invalid_token_data = {
        "grant_type": "password",
        "username": "auth-user",
        "password": "testpassword_invalid",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = client.post("/auth/token", data=invalid_token_data, headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_user_auth_token_request(client: TestClient):
    create_user(client)
    access_token = get_access_token(client)
    get_user_info(client, access_token)


def test_invalid_user_authentication(client: TestClient):
    get_access_token_invalid_user(client)
