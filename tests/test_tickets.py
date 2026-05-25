def authenticated_headers(client):
    client.post(
        "/auth/register",
        json={
            "name": "Ticket User",
            "email": "ticket@example.com",
            "password": "4343",
        },
    )
    response = client.post(
        "/auth/login",
        json={
            "email": "ticket@example.com",
            "password": "4343",
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_ticket_flow(client):
    headers = authenticated_headers(client)

    create_response = client.post(
        "/tickets",
        json={
            "title": "Erro ao acessar sistema",
            "description": "Usuario nao consegue acessar a conta",
            "priority": "ALTA",
        },
        headers=headers,
    )

    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]
    assert create_response.json()["status"] == "ABERTO"
    assert create_response.json()["priority"] == "ALTA"

    list_response = client.get("/tickets", headers=headers)

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.patch(
        f"/tickets/{ticket_id}/status",
        json={"status": "FINALIZADO"},
        headers=headers,
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "FINALIZADO"


def test_create_ticket_requires_token(client):
    response = client.post(
        "/tickets",
        json={
            "title": "Erro ao acessar sistema",
            "description": "Usuario nao consegue acessar a conta",
        },
    )

    assert response.status_code == 401


def test_delete_ticket(client):
    headers = authenticated_headers(client)
    create_response = client.post(
        "/tickets",
        json={
            "title": "Ticket para excluir",
            "description": "Descricao do ticket para excluir",
        },
        headers=headers,
    )
    ticket_id = create_response.json()["id"]

    delete_response = client.delete(f"/tickets/{ticket_id}", headers=headers)

    assert delete_response.status_code == 204

    list_response = client.get("/tickets", headers=headers)

    assert list_response.status_code == 200
    assert list_response.json() == []
