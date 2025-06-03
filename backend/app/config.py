# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    SUMMARY_MODEL: str = "gpt-4"

    class Config:
        env_file = "../.env"           # relative to this file
        env_file_encoding = "utf-8"

settings = Settings()
