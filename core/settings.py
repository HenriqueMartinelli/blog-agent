# app/core/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    TOPIC_API_URL: str = "https://api.fake-topics.dev/trending"
    TOPIC_API_KEY: str = "demo-key"

    DATABASE_URL: str = "postgresql+asyncpg://blog_user:senha123@localhost:5432/blog_db"

    DEV: bool = True
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file = "./.env",
        env_file_encoding="utf-8",
        frozen=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

settings = Settings()
