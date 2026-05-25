def test_register_and_login(client):
    register_response = client.post(
        "/auth/register",
        json={
            "name": "Kaique",
            "email": "kaique@example.com",
            "password": "4343",
        },
    )

    assert register_response.status_code == 201
    assert register_response.json()["email"] == "kaique@example.com"

    login_response = client.post(
        "/auth/login",
        json={
            "email": "kaique@example.com",
            "password": "4343",
        },
    )

    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"
    assert "access_token" in login_response.json()


def test_list_users_requires_token(client):
    response = client.get("/auth/users")

    assert response.status_code == 401
