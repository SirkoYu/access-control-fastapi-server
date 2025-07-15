from unittest.mock import patch
import pytest
from fastapi import status

from tests.conftest import hash_password
from src.models.user import User

@pytest.mark.asyncio
@patch("src.crud.user.hash_password", hash_password)
async def test_create_user(client, db_session):
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "first": "Test",
        "last": "User"
    }
    
    response = client.post("/api/user/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["first"] == user_data["first"]
    assert data["last"] == user_data["last"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_user(client, test_user):
    response = client.get(f"/api/user/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email

@pytest.mark.asyncio
@patch("src.crud.user.hash_password", hash_password)
async def test_update_user(client, test_user: User):
    update_data = {
        "password": "12345",
        "email": "updated@example.com",
        "first": "Updated",
        "last": "User",
        "is_active": True
    }
    response = client.put(
        f"/api/user/{test_user.id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["email"] == update_data["email"]
    assert data["first"] == update_data["first"]
    assert data["last"] == update_data["last"]
    assert data["is_active"] == update_data["is_active"]

@pytest.mark.asyncio
async def test_delete_user(client, test_user):
    response = client.delete(f"/api/user/{test_user.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Перевіряємо, що користувача більше немає
    response = client.get(f"/api/user/{test_user.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_users(client, test_user):
    response = client.get("/api/user/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(user["id"] == test_user.id for user in data)

@pytest.mark.asyncio
async def test_get_user_with_roles(client, test_user: User):
    response = client.get(f"/api/user/user-with-roles/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == test_user.id
    assert "roles" in data

@pytest.mark.asyncio
async def test_get_users_with_roles(client, test_user):
    response = client.get("/api/user/users-with-roles")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert any(user["id"] == test_user.id for user in data)
    assert all("roles" in user for user in data)