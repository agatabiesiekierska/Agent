## Configuration file for an fastapi app

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    openai_api_key: str 
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file= r"D:\Python\Agent\.env",
        env_ignore_empty=True,
        extra="ignore",
    )


settings = Settings()
