from pathlib import Path

from pydantic_settings import BaseSettings

BASE_PATH = Path(__file__).resolve().parent


class Settings(BaseSettings):
    BOT_TOKEN: str

    class Config:
        env_file = BASE_PATH / ".env"
