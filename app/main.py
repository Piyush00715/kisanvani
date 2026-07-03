from fastapi import FastAPI

app = FastAPI(title="KisanVani API")

@app.get("/")
def health_check():
    return {"status": "KisanVani backend running"}

# Yahan crop-rec, disease-detection, voice-sms ke routers include honge
