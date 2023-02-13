import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, "..")


class ProfileSettings(BaseSettings):
    calendar_id: str


class Settings(BaseSettings):
    profile: ProfileSettings

    class Config:
        env_file = (os.path.join(ENV_DIR, ".env"),)
        env_nested_delimiter = "__"


settings = Settings()
