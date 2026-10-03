from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.routes.auth import get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.database import db
from bson import ObjectId
import os
import shutil

router = APIRouter(prefix="/users", tags=["users"])

# Create uploads directory if it doesn't exist
os.makedirs("uploads/profiles", exist_ok=True)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user["_id"]),
        **current_user
    )

@router.put("/me", response_model=UserResponse)
async def update_me(update_data: UserUpdate, current_user: dict = Depends(get_current_user)):
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    if update_dict:
        await db.db["users"].update_one(
            {"_id": current_user["_id"]},
            {"$set": update_dict}
        )
        current_user.update(update_dict)
        
    return UserResponse(
        id=str(current_user["_id"]),
        **current_user
    )

@router.post("/me/photo")
async def upload_photo(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    ext = file.filename.split(".")[-1]
    if ext.lower() not in ["jpg", "jpeg", "png", "gif", "webp"]:
        raise HTTPException(status_code=400, detail="Invalid image format")
        
    filename = f"{current_user['_id']}.{ext}"
    file_path = f"uploads/profiles/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    photo_url = f"/uploads/profiles/{filename}"
    
    await db.db["users"].update_one(
        {"_id": current_user["_id"]},
        {"$set": {"photoUrl": photo_url}}
    )
    
    return {"photoUrl": photo_url}
