import pytest 
from httpx import AsyncClient
import logging

logger = logging.getLogger(__name__)

@pytest.mark.parametrize("payload, expected_status", [
    ({"email": "valid@test.com", "password": "correct_pass", "name": "Dima"}, 201),
    ({"email": "valid@test.com", "password": "correct_pass", "name": "Dima"}, 400),
])

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, payload, expected_status):  
    response = await client.post("/auth/register", json=payload)
    
    assert response.status_code == expected_status
        
        
    assert response.status_code == expected_status
    
@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    response = await client.post("/auth/login", json={"email": "valid@test.com", "password": "correct_pass", "name": "Dima"})

    assert response.status_code == 200