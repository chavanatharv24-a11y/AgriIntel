from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    password: str
    cropType: Optional[str] = None
    landSize: Optional[float] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    age: int
    email: EmailStr
    cropType: Optional[str] = None
    landSize: Optional[float] = None
    photoUrl: Optional[str] = None
    createdAt: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    cropType: Optional[str] = None
    landSize: Optional[float] = None
