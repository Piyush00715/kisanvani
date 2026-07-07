import io
import os
import json
import base64
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.routers.auth import save_user_history
import openai

router = APIRouter()

@router.post("/predict")
async def predict_disease(
    image: UploadFile = File(None),
    phone_number: str = Form(None),
    voice_note: str = Form(None)
):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key missing. Disease detection relies on OpenAI for analysis.")
    
    try:
        client = openai.OpenAI(api_key=openai_api_key)
        
        messages = [
            {"role": "system", "content": "You are an expert agricultural AI. Diagnose the plant disease based on the image or the farmer's voice description. Provide a detailed description, prevention steps, and suggest a relevant supplement. Reply strictly in JSON format with keys: 'disease', 'description', 'prevention', 'supplement_name'."}
        ]
        
        content_parts = []
        
        if voice_note:
            content_parts.append({"type": "text", "text": f"The farmer says: '{voice_note}'"})
            
        if image:
            contents = await image.read()
            base64_image = base64.b64encode(contents).decode('utf-8')
            content_parts.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            )
            content_parts.append({"type": "text", "text": "Analyze this image. If it does NOT clearly show a plant, crop, leaf, or agricultural field, set 'disease' to 'INVALID_IMAGE' and leave other fields empty."})
            
        if not content_parts:
            raise HTTPException(status_code=400, detail="Please provide an image or a voice note.")
            
        messages.append({"role": "user", "content": content_parts})
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=300
        )
        
        response_text = response.choices[0].message.content.strip()
        
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].strip()
            
        data = json.loads(response_text)
        
        if data.get("disease") == "INVALID_IMAGE":
            raise HTTPException(status_code=400, detail="Kripya kisi fasal, paudhe ya patte ki sahi photo upload karein.")
            
        title = data.get("disease", "Unknown Disease")
        description = data.get("description", "No description provided.")
        prevent = data.get("prevention", "No prevention details provided.")
        
        # Determine image URL based on whether they uploaded an image or just audio
        image_url = f"data:image/jpeg;base64,{base64_image}" if image else "https://lh3.googleusercontent.com/aida-public/AB6AXuDTKLYK8TbXxVmYuqnxOz4-S901osIXhf0RxOz4BZ3crV77wn9aZ2asZadq6ZsmvVibQh72QtnLuw3Ptq87hg3KCEIiUU0cmKsDQWAcZmCk_o8WF7dkqiBU8Ni-UlluXPT3fEmgnw0srpUdbxpDFZjoR1i_r7icmXTFWNxUCoq5lQoI4mL_akPAdhAdmoRXYnshiZLUltTBYhsguUKQPBnrjZML-j5mFQ0rkyaxEgfqAWhsKiMUalvM"
        
        supplement_name = data.get("supplement_name", "General Fertilizer")
        supplement_image_url = ""
        supplement_buy_link = "#"
        
        # Save History
        if phone_number:
            save_user_history(
                phone_number,
                "Disease Detection",
                f"Diagnosed: {title}",
                f"Description: {description} | Treatment: {prevent} | Supplement: {supplement_name}"
            )

        return {
            "title": title,
            "desc": description,
            "prevent": prevent,
            "image_url": image_url,
            "sname": supplement_name,
            "simage": supplement_image_url,
            "buy_link": supplement_buy_link
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print("Prediction error:", e)
        raise HTTPException(status_code=500, detail="Error analyzing the image or voice note.")
