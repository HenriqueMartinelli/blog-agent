
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str

    DATABASE_URL: str = "postgresql+asyncpg://blog_user:senha123@localhost:5432/blog_db"

    DEV: bool = True
    ENVIRONMENT: str = "development"

    LOG_FILE: str = "logs/app_logs.log"  
    REPORT_FILE: str = "logs/log_report.csv"  

    model_config = SettingsConfigDict(
        env_file = "./.env",
        env_file_encoding="utf-8",
        frozen=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)
        os.makedirs(os.path.dirname(self.REPORT_FILE), exist_ok=True)

settings = Settings()
