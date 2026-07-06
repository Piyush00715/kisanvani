import os
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Note: The OpenWeatherMap API key should be provided in environment variables
# export OPENWEATHERMAP_API_KEY="your_api_key_here"
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "")

from app.routers.auth import save_user_history

@router.get("/")
def get_weather(city: str, phone_number: str = None, soil_moisture: float = None):
    if not WEATHER_API_KEY:
        raise HTTPException(
            status_code=503, 
            detail="Weather API key is not configured on the server. Set OPENWEATHERMAP_API_KEY."
        )
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        
        # 1. Fetch Satellite Soil Moisture if not provided
        if soil_moisture is None:
            try:
                om_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=soil_moisture_0_to_7cm"
                om_resp = requests.get(om_url)
                if om_resp.status_code == 200:
                    om_data = om_resp.json()
                    volumetric_sm = om_data.get("current", {}).get("soil_moisture_0_to_7cm", 0.3)
                    soil_moisture = round(volumetric_sm * 100, 1)  # Convert to percentage
                else:
                    soil_moisture = 45.0  # Fallback
            except Exception:
                soil_moisture = 45.0
        
        # 2. Smart Advisory Logic
        advisory_title = "Field Status Optimal"
        advisory_desc = "Current conditions are suitable for general farm activities. Keep monitoring."
        
        if soil_moisture < 30 and "rain" not in weather_desc.lower():
            advisory_title = "Irrigation Alert"
            advisory_desc = f"Soil moisture is critically low ({soil_moisture}%). Immediate watering is recommended to prevent crop stress."
        elif soil_moisture > 70:
            advisory_title = "Drainage Warning"
            advisory_desc = f"High soil moisture detected ({soil_moisture}%). Avoid overwatering to prevent root rot or fungal diseases."
        elif temp > 35:
            advisory_title = "Heat Stress Warning"
            advisory_desc = f"Temperatures are soaring at {temp}°C. Ensure adequate irrigation and consider shading for sensitive crops."
        elif data["wind"]["speed"] > 5.0:
            advisory_title = "Spray Warning"
            advisory_desc = f"Wind speeds are high ({data['wind']['speed']} m/s). Avoid pesticide spraying to prevent chemical drift."
        elif "rain" in weather_desc.lower():
            advisory_title = "Rain Forecasted"
            advisory_desc = f"Expected {weather_desc}. Halt irrigation schedules to avoid waterlogging and save resources."
        
        advisory = f"<strong>{advisory_title}</strong>: {advisory_desc}"
        
        if phone_number:
            details_str = f"City: {city}, Temp: {temp}°C, Moisture: {soil_moisture}%"
            save_user_history(phone_number, "Weather Advisory", details_str)

        return {
            "city": data.get("name"),
            "temperature_celsius": temp,
            "humidity_percent": data["main"]["humidity"],
            "weather_condition": weather_desc,
            "wind_speed_m_s": data["wind"]["speed"],
            "advisory": advisory,
            "satellite_soil_moisture": soil_moisture
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch weather data: {str(e)}")
