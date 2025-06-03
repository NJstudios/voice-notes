# backend/app/audio_utils.py
import openai
import os
from .config import settings

# For newer versions of openai library (v1.0+)
try:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    OPENAI_V1 = True
except ImportError:
    # Fallback for older versions
    openai.api_key = settings.OPENAI_API_KEY
    OPENAI_V1 = False

def transcribe_file(path: str) -> dict:
    """
    Calls OpenAI's Whisper (via openai.Audio.transcribe). 
    Returns a dict: {"text": "...", "duration": ... }.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Audio file not found: {path}")
    
    print(f"Transcribing file: {path}")
    print(f"File size: {os.path.getsize(path)} bytes")
    
    try:
        with open(path, "rb") as audio_file:
            if OPENAI_V1:
                # New API (v1.0+)
                result = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                transcript_text = result.text
            else:
                # Old API (pre-v1.0)
                result = openai.Audio.transcribe(model="whisper-1", file=audio_file)
                if isinstance(result, dict):
                    transcript_text = result.get("text", "")
                else:
                    transcript_text = str(result)
        
        print(f"Transcription successful: {transcript_text[:100]}...")
        
        return {
            "text": transcript_text,
            "duration": 0.0  # Whisper API doesn't return duration by default
        }
            
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        print(f"Error type: {type(e)}")
        raise Exception(f"Transcription failed: {e}")