
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="ShopFlow Notification Service")

notifications = {}


class NotificationCreate(BaseModel):
    recipient: str = Field(min_length=1)
    message: str = Field(min_length=1)
    channel: str = Field(pattern="^(email|sms)$")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "notification-service",
    }


@app.post("/notifications", status_code=201)
def create_notification(notification: NotificationCreate):
    notification_id = str(uuid4())

    new_notification = {
        "notification_id": notification_id,
        "recipient": notification.recipient,
        "message": notification.message,
        "channel": notification.channel,
        "status": "queued",
    }

    notifications[notification_id] = new_notification

    return new_notification


@app.get("/notifications")
def list_notifications():
    return list(notifications.values())


@app.get("/notifications/{notification_id}")
def get_notification(notification_id: str):
    if notification_id not in notifications:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return notifications[notification_id]
