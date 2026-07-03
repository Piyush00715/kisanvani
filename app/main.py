# pyrefly: ignore [missing-import]
import os
from dotenv import load_dotenv

# Load .env file before anything else
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import crop_recommendation
from app.routers import disease_detection
from app.routers import weather_advisory
from app.routers import voice_sms

app = FastAPI(title="KisanVani API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "KisanVani backend running"}

app.include_router(crop_recommendation.router, prefix="/api/crop", tags=["Crop Recommendation"])
app.include_router(disease_detection.router, prefix="/api/disease", tags=["Disease Detection"])
app.include_router(weather_advisory.router, prefix="/api/weather", tags=["Weather Advisory"])
app.include_router(voice_sms.router, prefix="/api/communications", tags=["Voice & SMS"])
