import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_TITLE: str = "SkilledUp API"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "SkilledUp API"
    HOST_URL: str = os.environ.get("HOST_URL")
    HOST_PORT: int = int(os.environ.get("HOST_PORT"))
    DB_CONFIG: str = os.environ.get("DB_CONFIG")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = os.environ.get("ALGORITHM")


settings = Settings()
