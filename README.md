# KisanVani 🌾🎙️

Voice-and-SMS agricultural intelligence platform for small & marginal farmers, in Indic languages.

## 🌟 Problem Statement
Indian farmers, especially smallholders, face immense challenges due to unpredictable weather patterns, pest attacks, and lack of scientific crop planning. While vast amounts of agricultural data and AI tools exist, they are often inaccessible to rural farmers due to **language barriers**, **complex user interfaces**, and **poor digital literacy**. Farmers need timely, actionable, and localized intelligence in their native language to make informed decisions and prevent crop losses.

## 💡 Our Solution
**KisanVani** (Farmer's Voice) is a multi-lingual, AI-powered agricultural assistant designed specifically for the rural Indian demographic. It bridges the gap between advanced AI and grassroots farming by offering a highly intuitive, voice-first, and native-language interface. It proactively alerts farmers about critical weather events and provides instant, AI-driven diagnostics and crop planning directly on their mobile devices (via Web App or SMS).

## 🚀 Key Features

### 1. Intelligent Disease Detection (Scan Feature)
- Farmers can take a photo of a sick plant and add a voice note in their local language.
- The AI (OpenAI GPT-4o-mini Vision) cross-references visual symptoms with the voice description to provide the **Disease Name**, **Prevention Steps**, and **Recommended Supplements**.

### 2. Scientific Crop Recommendation
- Using a custom-trained **Random Forest ML model**, the system suggests the most scientifically viable crop based on Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, and Rainfall.

### 3. Automated Weather & Climate Alerts (Cron Jobs)
KisanVani proactively warns farmers via SMS in their local language.
- **Rain Alert:** Triggers if rainfall > 1mm is expected.
- **Dry Spell / Drought Alert:** Triggers if the average temperature is > 30°C and total rainfall is < 5mm over the next 5 days.
> **Note for Judges:** Due to Twilio Free Trial limits, live SMS testing is restricted to verified numbers. However, the identical logic is demonstrated visually on the **Weather Dashboard** in real-time. Below is a proof of the automated Twilio SMS alert sent to a verified farmer's number:
> 
> ![Twilio Dry Spell Alert Proof](frontend/assets/sms_proof.jpg)

### 4. Real-Time Weather Dashboard
- Fetches real-time localized weather data and 5-day forecasts based on GPS coordinates.

### 5. Agri-News Feed
- Fetches the latest agriculture-related news and uses AI to translate headlines into the farmer's chosen language.

### 6. RSK (Raitha Samparka Kendra) Expert Dashboard
- A specialized portal for agricultural experts to broadcast emergency warnings to registered farmers via translated SMS.
- **Access URL:** `/rsk` (e.g. `https://kisanvani.onrender.com/rsk`)
- **Login Credentials:** Username: `admin` | Password: `admin@123`

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, Tailwind CSS.
- **Backend:** FastAPI (Python), SQLite.
- **AI & ML:** Random Forest (Crop Recommendation), OpenAI GPT-4o-mini Vision (Disease Detection).
- **External Integrations:** Sarvam AI (Voice & Multilingual Translation), OpenWeatherMap API, Twilio API.

## ⚙️ Run locally
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```