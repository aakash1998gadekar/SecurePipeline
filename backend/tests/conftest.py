import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
from backend.app.database import engine, Base


@pytest_asyncio.fixture
async def client():
    # Create tables fresh for each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient):
    """Register a user and return auth headers."""
    await client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!",
    })
    response = await client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "SecurePass123!",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
