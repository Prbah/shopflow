from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "order-service",
    }


def test_create_order():
    response = client.post(
        "/orders",
        json={"product_id": 1, "quantity": 2},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["product_id"] == 1
    assert data["quantity"] == 2
    assert data["status"] == "created"
    assert "order_id" in data


def test_create_order_with_invalid_quantity():
    response = client.post(
        "/orders",
        json={"product_id": 1, "quantity": 0},
    )

    assert response.status_code == 422


def test_get_nonexistent_order():
    response = client.get("/orders/nonexistent-order-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_list_orders():
    client.post("/orders", json={"product_id": 2, "quantity": 3})

    response = client.get("/orders")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(
        order["product_id"] == 2 and order["quantity"] == 3
        for order in response.json()
    )
