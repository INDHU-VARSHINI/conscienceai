from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OFFLINE_MODE: bool = True
    OPENAI_API_KEY: str = ""
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = "../.env"

settings = Settings()
