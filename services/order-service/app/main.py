from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastAPI(title="ShopFlow Order Service")

orders = {}


class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "order-service"}


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    order_id = str(uuid4())

    new_order = {
        "order_id": order_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "created",
    }

    orders[order_id] = new_order
    return new_order


@app.get("/orders")
def list_orders():
    return list(orders.values())


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")

    return orders[order_id]
