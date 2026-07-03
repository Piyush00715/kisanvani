import os
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Note: The OpenWeatherMap API key should be provided in environment variables
# export OPENWEATHERMAP_API_KEY="your_api_key_here"
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "")

@router.get("/")
def get_weather(city: str):
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
        
        return {
            "city": data.get("name"),
            "temperature_celsius": data["main"]["temp"],
            "humidity_percent": data["main"]["humidity"],
            "weather_condition": data["weather"][0]["description"],
            "wind_speed_m_s": data["wind"]["speed"]
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch weather data: {str(e)}")
