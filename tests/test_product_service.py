import sys
from pathlib import Path

from fastapi.testclient import TestClient

SERVICE_DIR = (
    Path(__file__).resolve().parents[1]
    / "services"
    / "product-service"
)
sys.path.insert(0, str(SERVICE_DIR))

from main import app  # noqa: E402

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "product-service",
    }


def test_list_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_existing_product():
    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Mechanical Keyboard"


def test_missing_product_returns_404():
    response = client.get("/products/99999")

    assert response.status_code == 404


def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "USB-C Hub",
            "price": 1499,
            "description": "Seven-port USB-C hub",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "USB-C Hub"
    assert response.json()["id"] > 0


def test_reject_invalid_price():
    response = client.post(
        "/products",
        json={"name": "Invalid Product", "price": -10},
    )

    assert response.status_code == 422


def test_update_product():
    response = client.put(
        "/products/1",
        json={
            "name": "Updated Keyboard",
            "price": 2699,
            "description": "Updated product",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Keyboard"


def test_delete_product():
    create_response = client.post(
        "/products",
        json={"name": "Temporary Item", "price": 100},
    )
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"/products/{product_id}")

    assert delete_response.status_code == 204
    assert client.get(f"/products/{product_id}").status_code == 404
