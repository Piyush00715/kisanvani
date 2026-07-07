import os
import sqlite3
import requests
from fastapi import APIRouter
from app.routers.auth import DB_PATH, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from app.voice_sms.sarvam_service import translate_text

router = APIRouter()
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "")

@router.post("/trigger-dry-spell-alerts")
def trigger_dry_spell_alerts():
    if not WEATHER_API_KEY or not TWILIO_ACCOUNT_SID:
        return {"status": "error", "message": "Missing API keys for Weather or Twilio"}

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT phone_number, state, preferred_language, latitude, longitude FROM users")
    users = cursor.fetchall()
    conn.close()

    alerts_sent = 0
    for user in users:
        phone, state, lang, lat, lon = user
        
        # Determine coordinates or location string
        try:
            if lat and lon:
                weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
            else:
                weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={state}&appid={WEATHER_API_KEY}&units=metric"

            w_resp = requests.get(weather_url)
            if w_resp.status_code != 200:
                continue
            
            w_data = w_resp.json()
            weather_desc = w_data["weather"][0]["description"].lower()
            
            # Use fetched lat/lon if not in db
            if not lat or not lon:
                lat = w_data["coord"]["lat"]
                lon = w_data["coord"]["lon"]

            # Fetch Soil Moisture
            om_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=soil_moisture_0_to_7cm"
            om_resp = requests.get(om_url)
            soil_moisture = 50.0
            if om_resp.status_code == 200:
                om_data = om_resp.json()
                volumetric_sm = om_data.get("current", {}).get("soil_moisture_0_to_7cm", 0.5)
                soil_moisture = round(volumetric_sm * 100, 1)

            # Dry Spell Condition
            is_raining = "rain" in weather_desc or "drizzle" in weather_desc or "thunderstorm" in weather_desc
            if soil_moisture < 40.0 and not is_raining:
                alert_text = f"KisanVani Alert: Severe dry spell detected in your area. Soil moisture is critically low ({soil_moisture}%). Please irrigate your crops to prevent damage."
                
                # Translate if needed
                if lang != "en":
                    try:
                        translated = translate_text(alert_text, source_lang="en-IN", target_lang=f"{lang}-IN")
                        if translated:
                            alert_text = translated
                    except Exception as e:
                        print("Translation failed:", str(e))
                
                # Send SMS via Twilio
                url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
                data = {
                    "To": phone,
                    "From": TWILIO_PHONE_NUMBER,
                    "Body": alert_text
                }
                t_resp = requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
                if t_resp.status_code in [200, 201]:
                    alerts_sent += 1

        except Exception as e:
            print(f"Error processing user {phone}: {e}")

    return {"status": "success", "alerts_sent": alerts_sent}
