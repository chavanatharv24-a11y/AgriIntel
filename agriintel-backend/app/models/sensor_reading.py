from pydantic import BaseModel, Field
from datetime import datetime, timezone

class SensorReadingModel(BaseModel):
    userId: str
    deviceId: str
    soilMoisture: float
    temperature: float
    humidity: float
    rainDetected: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
