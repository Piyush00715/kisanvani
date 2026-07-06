"""
Temporary replacement for Bhashini (pending API approval). Swap back once Bhashini 
key is approved — same function interface, different provider.
"""
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")

def get_headers():
    return {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }

def speech_to_text_translate(audio_file_path, mode="translate"):
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {"api-subscription-key": SARVAM_API_KEY}
    
    with open(audio_file_path, "rb") as f:
        files = {"file": (os.path.basename(audio_file_path), f, "audio/wav")}
        data = {
            "model": "saaras:v3",
            "language_code": "hi-IN",
            "with_timestamps": "false"
        }
        response = requests.post(url, headers=headers, files=files, data=data)
        
        if response.status_code != 200:
            print("STT Error:", response.text)
            response.raise_for_status()
            
        res_json = response.json()
        return res_json.get("transcript", res_json.get("text", str(res_json)))

def translate_text(text, source_lang="en-IN", target_lang="hi-IN"):
    url = "https://api.sarvam.ai/translate"
    payload = {
        "input": text,
        "source_language_code": source_lang,
        "target_language_code": target_lang,
        "speaker_gender": "Male",
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": True
    }
    response = requests.post(url, headers=get_headers(), json=payload)
    if response.status_code != 200:
        print("Translate Error:", response.text)
        response.raise_for_status()
    res_json = response.json()
    return res_json.get("translated_text", str(res_json))

def text_to_speech(text, language_code="hi-IN", output_path="response.wav"):
    url = "https://api.sarvam.ai/text-to-speech"
    payload = {
        "inputs": [text],
        "target_language_code": language_code,
        "speaker": "priya",
        "pace": 1.0,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v3"
    }
    response = requests.post(url, headers=get_headers(), json=payload)
    if response.status_code != 200:
        print("TTS Error:", response.text)
        response.raise_for_status()
    res_json = response.json()
    
    audio_b64 = res_json.get("audios", [None])[0] or res_json.get("audio", "")
    
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(audio_b64))
    
    return output_path
