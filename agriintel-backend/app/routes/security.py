from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user
from app.database import db

router = APIRouter(prefix="/security", tags=["security"])

@router.get("/events")
async def get_security_events(current_user: dict = Depends(get_current_user)):
    events_cursor = db.db["security_events"].find().sort("timestamp", -1).limit(50)
    events = await events_cursor.to_list(length=50)
    
    # Convert ObjectId to string for JSON serialization
    for event in events:
        event["_id"] = str(event["_id"])
        
    return events
