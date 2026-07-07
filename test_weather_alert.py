import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

DB_PATH = "kisanvani.db"

def test_alert():
    if not TWILIO_ACCOUNT_SID:
        print("Error: Twilio credentials not found in .env")
        return
        
    # Get the first registered user's phone number
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT phone_number FROM users LIMIT 1")
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            print("Error: No users found in database. Please register on the website first.")
            return
            
        target_phone = user[0]
        
    except Exception as e:
        print(f"Database error: {e}")
        return

    print(f"Sending test alert to {target_phone}...")
    
    alert_text = "KisanVani Alert: Heavy rain or thunderstorm expected in your area (Testing). Please halt spraying and secure your harvested crops."
    
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = {
        "To": target_phone,
        "From": TWILIO_PHONE_NUMBER,
        "Body": alert_text
    }
    
    response = requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
    
    if response.status_code in [200, 201]:
        print("Success! Test SMS has been sent to your phone.")
    else:
        print(f"Failed to send SMS. Twilio Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_alert()
