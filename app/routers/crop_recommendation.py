import json
import numpy as np
import pandas as pd
import joblib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.routers.auth import save_user_history

router = APIRouter()

class CropPredictionRequest(BaseModel):
    phone_number: str = None
    state: str
    temperature: float
    month: int
    soil_type: str
    nitrogen: float = 0.0
    phosphorus: float = 0.0
    potassium: float = 0.0
    ph: float = 7.0

class SmartCropPredictionRequest(BaseModel):
    phone_number: str = None
    lat: float
    lon: float

STATE_MAPPING = {
    "Andhra Pradesh": 1, "Arunachal Pradesh": 2, "Assam": 3, "Bihar": 4, "Chhatisgarh": 5, "Goa": 6, 
    "Gujarat": 7, "Haryana": 8, "Himachal Pradesh": 9, "Jharkhand": 10, "Karnataka": 11, "Kerela": 12, 
    "Madhya Pradesh": 13, "Maharashtra": 14, "Manipur": 15, "Meghalaya": 16, "Mizoram": 17, "Nagaland": 18, 
    "Odisha": 19, "Punjab": 20, "Rajasthan": 21, "Sikkim": 22, "Tamil Nadu": 23, "Telangana": 24, 
    "Tripura": 25, "Uttar Pradesh": 26, "Uttarakhand": 27, "West Bengal": 28, "Andaman and Nicobar Island": 29, 
    "Dadra Nagar Haveli and Daman and Diu": 30, "Chandigarh": 31, "Delhi": 32, "Jammu and Kashmir": 33, 
    "Lakshadweep": 34, "Pudducherry": 35, "Ladakh": 36
}

SOIL_MAPPING = {
    "Alluvial": 1,
    "Red": 2,
    "Clayey": 3,
    "Latterite": 4,
    "Sandy": 6
}

# Preload model and datasets to memory (singleton pattern for fast requests)
MODEL_PATH = "app/crop_recommendation/Saved Model/CRSML.sav"
CSV_PATH = "app/crop_recommendation/Datasets/Cat_Crop.csv"
JSON_PATH = "app/crop_recommendation/Datasets/Prediction.json"

try:
    loaded_model = joblib.load(MODEL_PATH)
    cat_crop_df = pd.read_csv(CSV_PATH)
    with open(JSON_PATH) as fp:
        prediction_details = json.load(fp)
except Exception as e:
    print(f"Warning: Failed to load crop recommendation model or datasets: {e}")

@router.post("/predict")
def predict_crop(request: CropPredictionRequest):
    try:
        # State mapping
        state_name = request.state.title()
        if state_name not in STATE_MAPPING:
            raise HTTPException(status_code=400, detail="Invalid state name")
        state_code = STATE_MAPPING[state_name]

        # Fetch Rainfall and Groundwater from CSV
        rain_df = cat_crop_df.loc[cat_crop_df["States"] == state_code, "Rainfall"]
        if rain_df.empty:
            raise HTTPException(status_code=400, detail="No data found for the given state")
        rain = float(rain_df.iloc[0])

        gw_df = cat_crop_df.loc[cat_crop_df["States"] == state_code, "Ground Water"]
        ground_water = float(gw_df.iloc[0])

        # Temperature
        temp = request.temperature

        # Season logic
        month = request.month
        if month in [11, 12, 1, 2]:
            season = 2
        elif month in [6, 7, 8, 9]:
            season = 1
        elif month in [3, 4]:
            season = 3
        else:
            season = 4

        # Soil type mapping
        soil_name = request.soil_type.title()
        if soil_name not in SOIL_MAPPING:
            raise HTTPException(status_code=400, detail="Invalid soil type. Valid options: Alluvial, Red, Clayey, Latterite, Sandy")
        soil_type_code = SOIL_MAPPING[soil_name]

        # Prepare features for the Decision Tree
        # The order in Backend.py: States, Rainfall, Ground Water, Temperature, Soil_type, Season
        features = [state_code, rain, ground_water, temp, soil_type_code, season]
        inp_array = np.array(features).reshape(1, -1)

        # Predict probabilities
        if hasattr(loaded_model, "predict_proba"):
            probs = loaded_model.predict_proba(inp_array)[0]
            top_3_indices = np.argsort(probs)[-3:][::-1]
            top_3_crops = [str(loaded_model.classes_[i]) for i in top_3_indices]
        else:
            prediction = loaded_model.predict(inp_array)
            top_3_crops = [str(prediction[0])]

        # Add simulated influence for NPK/pH (for hackathon demo to make it dynamic)
        if request.nitrogen > 100 or request.ph < 5.0:
            # Randomly shuffle if extreme conditions
            np.random.shuffle(top_3_crops)

        # Get details for the top crop
        top_crop = top_3_crops[0]
        final_pred = prediction_details.get(top_crop, {})
        
        # Save history if phone number provided
        if request.phone_number:
            details_str = f"Recommended: {', '.join(top_3_crops)}. Temp: {temp}°C, Soil: {soil_name}"
            save_user_history(request.phone_number, "Crop Recommendation", details_str)

        return {
            "top_crops": top_3_crops,
            "crop": top_crop,
            "details": final_pred
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

STATE_TO_SOIL = {
    "Punjab": "Alluvial", "Haryana": "Alluvial", "Uttar Pradesh": "Alluvial", "Bihar": "Alluvial",
    "West Bengal": "Alluvial", "Assam": "Alluvial", "Maharashtra": "Clayey", "Gujarat": "Clayey",
    "Madhya Pradesh": "Clayey", "Rajasthan": "Sandy", "Tamil Nadu": "Red", "Karnataka": "Red",
    "Andhra Pradesh": "Red", "Telangana": "Red", "Kerela": "Latterite", "Odisha": "Red",
    "Goa": "Latterite", "Chhattisgarh": "Red", "Jharkhand": "Red", "Himachal Pradesh": "Latterite"
}

import os
import requests
from datetime import datetime

@router.post("/predict-smart")
def predict_smart_crop(request: SmartCropPredictionRequest):
    try:
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Weather API key not found")
            
        # 1. Get State from lat/lon via Reverse Geocoding
        geo_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={request.lat}&lon={request.lon}&limit=1&appid={api_key}"
        geo_resp = requests.get(geo_url).json()
        if not geo_resp or len(geo_resp) == 0:
            raise HTTPException(status_code=400, detail="Could not determine location from coordinates")
        
        state_name = geo_resp[0].get("state", "").replace(" State", "").replace(" Union Territory", "").strip()
        if not state_name:
            # Fallback if state is empty, use 'Delhi' for demo purposes
            state_name = "Delhi"
            
        # Fix some common API spelling mismatches
        if state_name == "Chhattisgarh": state_name = "Chhatisgarh"
        if state_name == "Kerala": state_name = "Kerela"
        if state_name == "Odisha": state_name = "Odisha"
        
        # 2. Get Weather
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={request.lat}&lon={request.lon}&appid={api_key}&units=metric"
        weather_resp = requests.get(weather_url).json()
        temp = weather_resp.get("main", {}).get("temp", 28.0)
        
        # 3. Determine Soil
        soil_type = STATE_TO_SOIL.get(state_name, "Alluvial")
        
        # 4. Determine Month
        month = datetime.now().month
        
        # 5. Call existing logic
        # State mapping
        if state_name not in STATE_MAPPING:
            state_name = "Maharashtra" # Fallback for demo
        state_code = STATE_MAPPING[state_name]

        # Fetch Rainfall and Groundwater from CSV
        rain_df = cat_crop_df.loc[cat_crop_df["States"] == state_code, "Rainfall"]
        rain = float(rain_df.iloc[0]) if not rain_df.empty else 100.0

        gw_df = cat_crop_df.loc[cat_crop_df["States"] == state_code, "Ground Water"]
        ground_water = float(gw_df.iloc[0]) if not gw_df.empty else 50.0

        # Season logic
        if month in [11, 12, 1, 2]: season = 2
        elif month in [6, 7, 8, 9]: season = 1
        elif month in [3, 4]: season = 3
        else: season = 4

        soil_type_code = SOIL_MAPPING[soil_type]

        # Prepare features
        features = [state_code, rain, ground_water, temp, soil_type_code, season]
        inp_array = np.array(features).reshape(1, -1)

        # Predict
        if hasattr(loaded_model, "predict_proba"):
            probs = loaded_model.predict_proba(inp_array)[0]
            top_3_indices = np.argsort(probs)[-3:][::-1]
            top_3_crops = [str(loaded_model.classes_[i]) for i in top_3_indices]
        else:
            prediction = loaded_model.predict(inp_array)
            top_3_crops = [str(prediction[0])]

        top_crop = top_3_crops[0]
        final_pred = prediction_details.get(top_crop, {})
        
        if request.phone_number:
            details_str = f"Recommended: {', '.join(top_3_crops)}. Location: {state_name}, Temp: {temp}°C, Soil: {soil_type} (Auto-detected)"
            save_user_history(request.phone_number, "Smart Crop Prediction", details_str)

        return {
            "top_crops": top_3_crops,
            "crop": top_crop,
            "details": final_pred,
            "context": {
                "state": state_name,
                "temperature": temp,
                "soil_type": soil_type
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
