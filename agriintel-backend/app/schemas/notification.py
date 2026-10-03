from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    message: str

class NotificationResponse(BaseModel):
    id: str
    userId: str
    message: str
    isRead: bool
    createdAt: datetime
