from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AIRecommendationResponse(BaseModel):
    id: str
    userId: str
    basedOnReadingId: Optional[str] = None
    recommendationText: str
    riskLevel: str
    createdAt: datetime
