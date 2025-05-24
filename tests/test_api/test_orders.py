import pytest
from fastapi import status

def test_create_order(client):
    # First create a product
    product_response = client.post(
        "/api/v1/products/",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 100,
            "category_id": 1
        }
    )
    product_id = product_response.json()["id"]
    
    # Then create an order
    response = client.post(
        "/api/v1/orders/",
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2
                }
            ],
            "shipping_address": "123 Test St",
            "payment_method": "credit_card"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 2

def test_get_orders(client):
    response = client.get("/api/v1/orders/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_get_order(client):
    # First create a product
    product_response = client.post(
        "/api/v1/products/",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 100,
            "category_id": 1
        }
    )
    product_id = product_response.json()["id"]
    
    # Then create an order
    create_response = client.post(
        "/api/v1/orders/",
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2
                }
            ],
            "shipping_address": "123 Test St",
            "payment_method": "credit_card"
        }
    )
    order_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == order_id
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id

def test_update_order_status(client):
    # First create a product
    product_response = client.post(
        "/api/v1/products/",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 100,
            "category_id": 1
        }
    )
    product_id = product_response.json()["id"]
    
    # Then create an order
    create_response = client.post(
        "/api/v1/orders/",
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2
                }
            ],
            "shipping_address": "123 Test St",
            "payment_method": "credit_card"
        }
    )
    order_id = create_response.json()["id"]
    
    # Then update its status
    response = client.patch(
        f"/api/v1/orders/{order_id}/status",
        json={"status": "shipped"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "shipped" 