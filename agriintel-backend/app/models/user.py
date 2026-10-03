from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import Optional

class UserModel(BaseModel):
    name: str
    age: int
    email: EmailStr
    password: str
    cropType: Optional[str] = None
    landSize: Optional[float] = None
    photoUrl: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
