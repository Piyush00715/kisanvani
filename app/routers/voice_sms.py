import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Environment variables for API keys
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
BHASHINI_API_KEY = os.getenv("BHASHINI_API_KEY", "")

class SMSRequest(BaseModel):
    phone_number: str
    message: str

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

@router.post("/send-sms")
def send_sms(request: SMSRequest):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        raise HTTPException(status_code=503, detail="Twilio credentials not configured.")
    
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = {
        "To": request.phone_number,
        "From": TWILIO_PHONE_NUMBER,
        "Body": request.message
    }
    
    try:
        response = requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        response.raise_for_status()
        return {"status": "success", "message": "SMS sent successfully."}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send SMS: {str(e)}")

from app.voice_sms.sarvam_service import translate_text as sarvam_translate

@router.post("/translate")
def translate_text(request: TranslationRequest):
    # Temporary fallback to Sarvam AI while Bhashini is pending
    try:
        translated = sarvam_translate(
            text=request.text, 
            source_lang=request.source_language, 
            target_lang=request.target_language
        )
        return {
            "status": "success",
            "original_text": request.text,
            "translated_text": translated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
