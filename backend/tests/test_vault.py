import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_secret(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/vault/secrets",
        json={"title": "API Key", "value": "sk-test-12345"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "API Key"
    assert "value" not in data  # Should not expose encrypted value in list response


@pytest.mark.asyncio
async def test_list_secrets(client: AsyncClient, auth_headers: dict):
    await client.post(
        "/api/vault/secrets",
        json={"title": "Secret 1", "value": "value1"},
        headers=auth_headers,
    )
    response = await client.get("/api/vault/secrets", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_get_secret_decrypted(client: AsyncClient, auth_headers: dict):
    create_resp = await client.post(
        "/api/vault/secrets",
        json={"title": "My Secret", "value": "super-secret-value"},
        headers=auth_headers,
    )
    secret_id = create_resp.json()["id"]

    response = await client.get(f"/api/vault/secrets/{secret_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["value"] == "super-secret-value"


@pytest.mark.asyncio
async def test_update_secret(client: AsyncClient, auth_headers: dict):
    create_resp = await client.post(
        "/api/vault/secrets",
        json={"title": "Old Title", "value": "old-value"},
        headers=auth_headers,
    )
    secret_id = create_resp.json()["id"]

    response = await client.put(
        f"/api/vault/secrets/{secret_id}",
        json={"title": "New Title"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


@pytest.mark.asyncio
async def test_delete_secret(client: AsyncClient, auth_headers: dict):
    create_resp = await client.post(
        "/api/vault/secrets",
        json={"title": "To Delete", "value": "delete-me"},
        headers=auth_headers,
    )
    secret_id = create_resp.json()["id"]

    response = await client.delete(f"/api/vault/secrets/{secret_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_resp = await client.get(f"/api/vault/secrets/{secret_id}", headers=auth_headers)
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/api/vault/secrets")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_cannot_access_other_users_secret(client: AsyncClient, auth_headers: dict):
    # Create secret as testuser
    create_resp = await client.post(
        "/api/vault/secrets",
        json={"title": "Private", "value": "mine"},
        headers=auth_headers,
    )
    secret_id = create_resp.json()["id"]

    # Register second user
    await client.post("/api/auth/register", json={
        "username": "otheruser",
        "email": "other@example.com",
        "password": "OtherPass123!",
    })
    login_resp = await client.post("/api/auth/login", data={
        "username": "otheruser",
        "password": "OtherPass123!",
    })
    other_headers = {"Authorization": f"Bearer {login_resp.json()['access_token']}"}

    # Try to access first user's secret
    response = await client.get(f"/api/vault/secrets/{secret_id}", headers=other_headers)
    assert response.status_code == 404
