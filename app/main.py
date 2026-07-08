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
from app.routers import news
from app.routers import auth
from app.routers import cron_jobs
from app.routers import rsk

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI(title="KisanVani API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint redirects to the dashboard HTML
@app.get("/")
def read_root():
    return RedirectResponse(url="/index.html")

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "admin@123")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/rsk")
def read_rsk(username: str = Depends(get_current_username)):
    from fastapi.responses import FileResponse
    return FileResponse("frontend/rsk_dashboard.html")

# Health check at /api/health
@app.get("/api/health")
def health_check():
    return {"status": "KisanVani backend running"}

# Include routers
app.include_router(crop_recommendation.router, prefix="/api/crop", tags=["Crop Recommendation"])
app.include_router(disease_detection.router, prefix="/api/disease", tags=["Disease Detection"])
app.include_router(weather_advisory.router, prefix="/api/weather", tags=["Weather Advisory"])
app.include_router(news.router, prefix="/api/news", tags=["Agri-News"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(cron_jobs.router, prefix="/api/cron", tags=["Cron Jobs"])
app.include_router(rsk.router, prefix="/api/rsk", tags=["RSK Expert Dashboard"])

# Mount static files (this must be at the end so it doesn't shadow /api/ routes)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
