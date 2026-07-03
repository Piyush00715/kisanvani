# KisanVani 🌾🎙️

Voice-and-SMS agricultural intelligence platform for small & marginal farmers, in Indic languages.

## Tech Stack
- Backend: Python (FastAPI) — single unified service
- Crop Recommendation: ML model (soil/rainfall/groundwater based)
- Disease Detection: PyTorch CNN (photo-based diagnosis)
- Voice/SMS/Translation: Bhashini API + Twilio

## Run locally
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
