import os
import random
import sqlite3
import requests
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Setup SQLite Database
DB_PATH = "kisanvani.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            state TEXT NOT NULL,
            preferred_language TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# In-memory store for OTPs (For production, use Redis or DB with expiry)
otp_store = {}

# Dependencies
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

class SendOTPRequest(BaseModel):
    phone_number: str

class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str

class RegisterRequest(BaseModel):
    phone_number: str
    state: str

def get_language_for_state(state: str) -> str:
    hindi_states = ["Punjab", "Rajasthan", "Uttar Pradesh", "Bihar", "Madhya Pradesh", "Haryana", "Jharkhand", "Chhattisgarh", "Uttarakhand", "Delhi"]
    if state in hindi_states:
        return "hi" # Hindi
    return "en" # Default to English for others (can be enhanced later)

@router.post("/send-otp")
def send_otp(request: SendOTPRequest):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        raise HTTPException(status_code=503, detail="Twilio credentials not configured.")
    
    phone = request.phone_number.strip()
    # Format to E.164 (Assuming India +91 for this demo if missing)
    if len(phone) == 10 and phone.isdigit():
        phone = f"+91{phone}"
    elif not phone.startswith("+"):
        phone = f"+{phone}"

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    otp_store[phone] = otp

    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = {
        "To": phone,
        "From": TWILIO_PHONE_NUMBER,
        "Body": f"Your KisanVani login OTP is: {otp}"
    }
    
    try:
        response = requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        response.raise_for_status()
        return {"status": "success", "message": "OTP sent successfully."}
    except requests.exceptions.RequestException as e:
        # Catch errors (e.g. unverified trial number or missing funds)
        # We allow it to pass so they can use the master OTP '123456'
        print(f"Twilio SMS Failed: {e}")
        return {"status": "success", "message": "OTP generated locally (Twilio SMS failed, please use master OTP 123456)."}

@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest):
    phone = request.phone_number.strip()
    if len(phone) == 10 and phone.isdigit():
        phone = f"+91{phone}"
    elif not phone.startswith("+"):
        phone = f"+{phone}"

    if phone not in otp_store or otp_store[phone] != request.otp:
        # For testing, let's allow a master OTP "123456" in case SMS fails
        if request.otp != "123456":
            raise HTTPException(status_code=400, detail="Invalid or expired OTP.")
    
    # OTP verified, remove from store
    if phone in otp_store:
        del otp_store[phone]

    # Check if user exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT state, preferred_language FROM users WHERE phone_number = ?", (phone,))
    user = cursor.fetchone()
    conn.close()

    if user:
        # User exists, return token and lang
        return {
            "status": "success", 
            "is_new_user": False,
            "token": f"token_{phone}", # Dummy token for MVP
            "preferred_language": user[1]
        }
    else:
        # User does not exist, prompt for registration
        return {
            "status": "success",
            "is_new_user": True
        }

@router.post("/register")
def register_user(request: RegisterRequest):
    phone = request.phone_number.strip()
    if len(phone) == 10 and phone.isdigit():
        phone = f"+91{phone}"
    elif not phone.startswith("+"):
        phone = f"+{phone}"

    lang = get_language_for_state(request.state)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (phone_number, state, preferred_language) VALUES (?, ?, ?)",
            (phone, request.state, lang)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="User already registered.")
    
    conn.close()

    return {
        "status": "success",
        "token": f"token_{phone}",
        "preferred_language": lang
    }
