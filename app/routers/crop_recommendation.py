import json
import numpy as np
import pandas as pd
import joblib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class CropPredictionRequest(BaseModel):
    state: str
    temperature: float
    month: int
    soil_type: str

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

        # Predict
        prediction = loaded_model.predict(inp_array)
        pred_crop_name = str(prediction[0])

        # Get details
        final_pred = prediction_details.get(pred_crop_name, {})

        return {
            "crop": pred_crop_name,
            "details": final_pred
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
