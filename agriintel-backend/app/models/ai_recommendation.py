from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class AIRecommendationModel(BaseModel):
    userId: str
    basedOnReadingId: Optional[str] = None
    recommendationText: str
    riskLevel: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
