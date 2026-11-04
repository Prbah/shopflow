from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "payment-service",
    }


def test_create_payment():
    response = client.post(
        "/payments",
        json={"order_id": "order-123", "amount": 250.50},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["order_id"] == "order-123"
    assert data["amount"] == 250.50
    assert data["status"] == "successful"
    assert "payment_id" in data


def test_create_payment_with_invalid_amount():
    response = client.post(
        "/payments",
        json={"order_id": "order-123", "amount": 0},
    )

    assert response.status_code == 422


def test_get_nonexistent_payment():
    response = client.get("/payments/nonexistent-payment-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


def test_list_payments():
    client.post(
        "/payments",
        json={"order_id": "order-456", "amount": 100},
    )

    response = client.get("/payments")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(
        payment["order_id"] == "order-456"
        and payment["amount"] == 100
        for payment in response.json()
    )
