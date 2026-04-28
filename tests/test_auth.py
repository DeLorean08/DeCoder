import pytest 
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):  
    response = await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "strong_password",
        "name": "testuser"
    })
    assert response.status_code == 201