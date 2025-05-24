import pytest
from fastapi import status

def test_login_wrong_password(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_wrong_email(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@example.com", "password": "testpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "password" not in data 