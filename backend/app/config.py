from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    OFFLINE_MODE: bool = True
    OPENAI_API_KEY: str = ""
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    PROJECT_ROOT: str = str(Path(__file__).resolve().parent)

    class Config:
        env_file = "../.env"

settings = Settings()
