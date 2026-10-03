from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class SecurityEventModel(BaseModel):
    email: str
    success: bool
    ipAddress: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
