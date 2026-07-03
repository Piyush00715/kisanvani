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

@router.post("/translate")
def translate_text(request: TranslationRequest):
    if not BHASHINI_API_KEY:
        raise HTTPException(status_code=503, detail="Bhashini API key not configured.")
        
    # Bhashini API integration would go here.
    # The actual endpoint structure depends on the Bhashini API pipeline being used.
    # This is a stub for the integration.
    
    return {
        "status": "success",
        "original_text": request.text,
        "translated_text": f"[Translated to {request.target_language} using Bhashini: {request.text}]"
    }
