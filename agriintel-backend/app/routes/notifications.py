from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.routes.auth import get_current_user
from app.database import db
from app.models.notification import NotificationModel

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("", response_model=NotificationResponse)
async def create_notification(notification: NotificationCreate, current_user: dict = Depends(get_current_user)):
    notification_model = NotificationModel(
        userId=str(current_user["_id"]),
        message=notification.message
    )
    notification_dict = notification_model.model_dump()
    result = await db.db["notifications"].insert_one(notification_dict)
    
    return NotificationResponse(
        id=str(result.inserted_id),
        **notification_dict
    )

@router.get("", response_model=List[NotificationResponse])
async def get_notifications(current_user: dict = Depends(get_current_user)):
    cursor = db.db["notifications"].find({"userId": str(current_user["_id"])}).sort("createdAt", -1)
    notifications = await cursor.to_list(length=100)
    
    response_list = []
    for n in notifications:
        response_list.append(NotificationResponse(
            id=str(n["_id"]),
            **n
        ))
    return response_list

@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(notification_id: str, current_user: dict = Depends(get_current_user)):
    try:
        obj_id = ObjectId(notification_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid notification ID format")
        
    notification = await db.db["notifications"].find_one({"_id": obj_id})
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    if notification["userId"] != str(current_user["_id"]):
        raise HTTPException(status_code=404, detail="Notification not found")
        
    await db.db["notifications"].update_one(
        {"_id": obj_id},
        {"$set": {"isRead": True}}
    )
    
    notification["isRead"] = True
    
    return NotificationResponse(
        id=str(notification["_id"]),
        **notification
    )
