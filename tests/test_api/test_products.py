import pytest
from fastapi import status

def test_create_product(client, db):
    response = client.post(
        "/api/v1/products/",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 100,
            "category_id": 1
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 99.99
    assert "id" in data

def test_get_products(client):
    response = client.get("/api/v1/products/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_get_product(client):
    # First create a product
    create_response = client.post(
        "/api/v1/products/",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 100,
            "category_id": 1
        }
    )
    product_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Test Product"

def test_update_product(client):
    # First create a product
    create_response = client.post(
        "/api/v1/products/",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 100,
            "category_id": 1
        }
    )
    product_id = create_response.json()["id"]
    
    # Then update it
    response = client.put(
        f"/api/v1/products/{product_id}",
        json={
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 149.99,
            "stock": 50,
            "category_id": 1
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 149.99

def test_delete_product(client):
    # First create a product
    create_response = client.post(
        "/api/v1/products/",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 100,
            "category_id": 1
        }
    )
    product_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND 