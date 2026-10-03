from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorReadingCreate(BaseModel):
    deviceId: str
    soilMoisture: float
    temperature: float
    humidity: float
    rainDetected: bool

class SensorReadingResponse(SensorReadingCreate):
    id: str
    userId: str
    timestamp: datetime
