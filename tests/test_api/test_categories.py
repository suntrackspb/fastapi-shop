import pytest
from fastapi import status

def test_create_category(client):
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": "Test Category",
            "description": "Test Category Description"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Category"
    assert "id" in data

def test_get_categories(client):
    response = client.get("/api/v1/categories/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_get_category(client):
    # First create a category
    create_response = client.post(
        "/api/v1/categories/",
        json={
            "name": "Test Category",
            "description": "Test Category Description"
        }
    )
    category_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "Test Category"

def test_update_category(client):
    # First create a category
    create_response = client.post(
        "/api/v1/categories/",
        json={
            "name": "Test Category",
            "description": "Test Category Description"
        }
    )
    category_id = create_response.json()["id"]
    
    # Then update it
    response = client.put(
        f"/api/v1/categories/{category_id}",
        json={
            "name": "Updated Category",
            "description": "Updated Category Description"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Category"
    assert data["description"] == "Updated Category Description"

def test_delete_category(client):
    # First create a category
    create_response = client.post(
        "/api/v1/categories/",
        json={
            "name": "Test Category",
            "description": "Test Category Description"
        }
    )
    category_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/categories/{category_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND 