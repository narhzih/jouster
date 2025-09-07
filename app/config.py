from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    database_url: str = ""
    log_level: str = "INFO"
    max_text_length: int = 50000

    class Config:
        env_file = ".env"


settings = Settings()
