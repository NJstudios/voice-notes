# app/audio_utils.py
import os
from datetime import datetime
import openai

from .config import settings

openai.api_key = settings.OPENAI_API_KEY

def transcribe_file(temp_path: str) -> dict:
    """
    Calls OpenAI Whisper to transcribe the given audio file.
    Returns a dict with keys: text, duration (if available).
    """
    with open(temp_path, "rb") as f:
        res = openai.Audio.transcribe(model="whisper-1", file=f)
    return res
