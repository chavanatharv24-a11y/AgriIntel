from pydantic import BaseModel, Field
from datetime import datetime, timezone

class NotificationModel(BaseModel):
    userId: str
    message: str
    isRead: bool = False
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
