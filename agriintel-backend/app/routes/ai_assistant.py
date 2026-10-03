from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from app.config import settings
from app.routes.auth import get_current_user

router = APIRouter(prefix="/ai-assistant", tags=["ai-assistant"])

genai.configure(api_key=settings.GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str
    language: str = "en"

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agronomist(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    """
    Chat with the AI Agronomist. 
    It takes a farmer's question and returns practical farming advice.
    """
    lang_instruction = {
        "en": "Reply in English.",
        "hi": "Reply in Hindi.",
        "mr": "Reply in Marathi.",
        "es": "Reply in Spanish."
    }.get(request.language, "Reply in English.")

    prompt = f"""
You are "Agri", a friendly, highly experienced virtual agronomist. 
You are talking to a farmer who is using a mobile app.
Keep your answers extremely practical, short (under 3 sentences if possible), and easy to understand.
Do not use overly complex scientific jargon.

Farmer asks: "{request.message}"

{lang_instruction}
"""
    model = genai.GenerativeModel("gemini-flash-latest")
    try:
        response = model.generate_content(prompt)
        return ChatResponse(reply=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
