from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.sensor_reading import SensorReadingCreate, SensorReadingResponse
from app.routes.auth import get_current_user
from app.database import db
from app.models.sensor_reading import SensorReadingModel

router = APIRouter(prefix="/sensor", tags=["sensors"])

@router.post("/readings", response_model=SensorReadingResponse)
async def create_reading(reading: SensorReadingCreate, current_user: dict = Depends(get_current_user)):
    reading_model = SensorReadingModel(
        userId=str(current_user["_id"]),
        **reading.model_dump()
    )
    reading_dict = reading_model.model_dump()
    result = await db.db["sensor_readings"].insert_one(reading_dict)
    
    return SensorReadingResponse(
        id=str(result.inserted_id),
        **reading_dict
    )

@router.get("/readings", response_model=List[SensorReadingResponse])
async def get_readings(current_user: dict = Depends(get_current_user)):
    cursor = db.db["sensor_readings"].find({"userId": str(current_user["_id"])}).sort("timestamp", -1)
    readings = await cursor.to_list(length=100)
    
    response_list = []
    for r in readings:
        response_list.append(SensorReadingResponse(
            id=str(r["_id"]),
            **r
        ))
    return response_list
