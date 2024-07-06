from pathlib import Path

from pydantic_settings import BaseSettings

BASE_PATH = Path(__file__).resolve().parent


class Settings(BaseSettings):
    DISCORD_TOKEN: str
    HUGGING_FACE_TOKEN: str
    GEMINI_API_KEY: str

    class Config:
        env_file = BASE_PATH / ".env"
