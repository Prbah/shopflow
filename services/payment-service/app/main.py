from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="ShopFlow Payment Service")

payments = {}


class PaymentCreate(BaseModel):
    order_id: str
    amount: float = Field(gt=0)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "payment-service",
    }


@app.post("/payments", status_code=201)
def create_payment(payment: PaymentCreate):
    payment_id = str(uuid4())

    new_payment = {
        "payment_id": payment_id,
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": "successful",
    }

    payments[payment_id] = new_payment
    return new_payment


@app.get("/payments")
def list_payments():
    return list(payments.values())


@app.get("/payments/{payment_id}")
def get_payment(payment_id: str):
    if payment_id not in payments:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    return payments[payment_id]
