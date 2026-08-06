import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post("/api/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "StrongPass99!",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_user(client: AsyncClient):
    payload = {
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "StrongPass99!",
    }
    await client.post("/api/auth/register", json=payload)
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await client.post("/api/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "StrongPass99!",
    })
    response = await client.post("/api/auth/login", data={
        "username": "loginuser",
        "password": "StrongPass99!",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post("/api/auth/register", json={
        "username": "wrongpw",
        "email": "wrong@example.com",
        "password": "StrongPass99!",
    })
    response = await client.post("/api/auth/login", data={
        "username": "wrongpw",
        "password": "WrongPassword!",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    response = await client.post("/api/auth/register", json={
        "username": "weakpw",
        "email": "weak@example.com",
        "password": "short",
    })
    assert response.status_code == 422
