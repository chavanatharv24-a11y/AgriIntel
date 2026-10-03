from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import google.generativeai as genai
import re
from app.config import settings
from app.database import db
from app.routes.auth import get_current_user
from app.models.ai_recommendation import AIRecommendationModel
from app.schemas.ai_recommendation import AIRecommendationResponse

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

genai.configure(api_key=settings.GEMINI_API_KEY)

@router.post("/generate", response_model=AIRecommendationResponse)
async def generate_recommendation(lang: str = "en", current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    
    # Fetch most recent reading
    cursor = db.db["sensor_readings"].find({"userId": user_id}).sort("timestamp", -1).limit(1)
    readings = await cursor.to_list(length=1)
    
    if not readings:
        raise HTTPException(status_code=404, detail="No sensor readings found for this user. Cannot generate recommendations.")
        
    reading = readings[0]
    
    # Build prompt
    lang_instruction = "Please reply in Marathi." if lang == "mr" else "Please reply in Hindi." if lang == "hi" else "Please reply in English."
    
    prompt = f"""
You are an expert agronomist providing concise, farmer-friendly advice.
Based on the following sensor reading from a crop field:
- Soil Moisture: {reading.get('soilMoisture')}%
- Temperature: {reading.get('temperature')}°C
- Humidity: {reading.get('humidity')}%
- Rain Detected: {'Yes' if reading.get('rainDetected') else 'No'}

Please provide:
1. Irrigation advice
2. Fertilizer advice
3. Risk level for the crop

IMPORTANT: State the risk level clearly on its own line exactly in this format in English (regardless of response language):
Risk Level: [Low/Medium/High]

{lang_instruction}
"""
    
    model = genai.GenerativeModel("gemini-flash-latest")
    try:
        response = model.generate_content(prompt)
        ai_text = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with AI service: {str(e)}")
        
    # Extract risk level
    risk_level = "Unknown"
    match = re.search(r"Risk Level:\s*(Low|Medium|High)", ai_text, re.IGNORECASE)
    if match:
        risk_level = match.group(1).capitalize()
        
    # Save recommendation
    rec_model = AIRecommendationModel(
        userId=user_id,
        basedOnReadingId=str(reading["_id"]),
        recommendationText=ai_text,
        riskLevel=risk_level
    )
    
    rec_dict = rec_model.model_dump()
    result = await db.db["ai_recommendations"].insert_one(rec_dict)
    
    return AIRecommendationResponse(
        id=str(result.inserted_id),
        **rec_dict
    )

@router.post("/diagnose", response_model=AIRecommendationResponse)
async def diagnose_disease(lang: str = "en", image: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    image_bytes = await image.read()
    
    lang_instruction = "Please reply in Marathi." if lang == "mr" else "Please reply in Hindi." if lang == "hi" else "Please reply in English."
    
    prompt = f"""Identify any visible crop disease, state a confidence level, and give a one-paragraph treatment recommendation.
IMPORTANT: State the disease name clearly on its own line exactly in this format in English (regardless of response language):
Disease: [name or 'None detected']

{lang_instruction}"""
    
    model = genai.GenerativeModel("gemini-flash-latest")
    try:
        response = model.generate_content([
            prompt,
            {"mime_type": image.content_type or "image/jpeg", "data": image_bytes}
        ])
        ai_text = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with AI service: {str(e)}")
        
    disease_name = "Unknown"
    match = re.search(r"Disease:\s*(.+)", ai_text, re.IGNORECASE)
    if match:
        disease_name = match.group(1).strip()
        
    rec_model = AIRecommendationModel(
        userId=user_id,
        basedOnReadingId=None,
        recommendationText=ai_text,
        riskLevel=disease_name
    )
    
    rec_dict = rec_model.model_dump()
    result = await db.db["ai_recommendations"].insert_one(rec_dict)
    
    return AIRecommendationResponse(
        id=str(result.inserted_id),
        **rec_dict
    )
