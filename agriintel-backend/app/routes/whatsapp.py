from fastapi import APIRouter, Request, Response
import google.generativeai as genai
from app.config import settings

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Twilio WhatsApp Webhook endpoint.
    Receives incoming messages/images from farmers via WhatsApp and replies.
    """
    form_data = await request.form()
    
    incoming_msg = form_data.get('Body', '').lower()
    media_url = form_data.get('MediaUrl0')
    sender = form_data.get('From')
    
    # In a real app, we would download media_url, pass it to Gemini, and use Twilio API to send the response.
    # For now, this is a skeleton endpoint.
    
    response_text = "Namaskar! AgriIntel WhatsApp bot active. Please send a photo of your crop to get an AI diagnosis."
    if media_url:
        response_text = "We received your photo! Our AI is analyzing it and will get back to you shortly."
        
    # Twilio expects TwiML XML response
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{response_text}</Message>
</Response>"""

    return Response(content=twiml_response, media_type="application/xml")
