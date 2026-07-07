import sys
from app.voice_sms.sarvam_service import translate_text, text_to_speech

def test():
    try:
        sample_text = "Hello, welcome to KisanVani. We are testing the new Sarvam AI system."
        print(f"Original Text: {sample_text}")
        
        # Test translation
        print("Translating to Hindi...")
        translated = translate_text(sample_text, source_lang="en-IN", target_lang="hi-IN")
        print(f"Translated Text: {translated}")
        
        # Test TTS
        print("Converting to Speech...")
        output_file = "test_output.wav"
        text_to_speech(translated, language_code="hi-IN", output_path=output_file)
        print(f"Saved audio to {output_file}")
        
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test()
