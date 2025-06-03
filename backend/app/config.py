# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    SUMMARY_MODEL: str = "gpt-4"

    class Config:
             _file = "../.env"

settings = Settings()
