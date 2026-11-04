from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "notification-service",
    }


def test_create_notification():
    payload = {
        "recipient": "user@example.com",
        "message": "Your order has been created.",
        "channel": "email",
    }

    response = client.post("/notifications", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["recipient"] == payload["recipient"]
    assert data["message"] == payload["message"]
    assert data["channel"] == payload["channel"]
    assert data["status"] == "queued"
    assert "notification_id" in data


def test_create_notification_with_invalid_channel():
    payload = {
        "recipient": "user@example.com",
        "message": "Your order has been created.",
        "channel": "whatsapp",
    }

    response = client.post("/notifications", json=payload)

    assert response.status_code == 422


def test_create_notification_with_empty_message():
    payload = {
        "recipient": "user@example.com",
        "message": "",
        "channel": "email",
    }

    response = client.post("/notifications", json=payload)

    assert response.status_code == 422


def test_get_nonexistent_notification():
    response = client.get("/notifications/nonexistent-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Notification not found"


def test_list_notifications():
    payload = {
        "recipient": "user@example.com",
        "message": "Your payment was successful.",
        "channel": "email",
    }

    create_response = client.post("/notifications", json=payload)
    notification_id = create_response.json()["notification_id"]

    response = client.get("/notifications")

    assert response.status_code == 200
    assert any(
        notification["notification_id"] == notification_id
        for notification in response.json()
    )
