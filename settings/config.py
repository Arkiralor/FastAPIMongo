import logging
from os import path, makedirs
from pydantic import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):

    APP_NAME: str
    APP_URI: str
    ENV_TYPE:str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    OWNER_EMAIL: str
    MONGODB_URL: str
    MONGO_URI: str
    MONGO_NAME:str
    MONGO_HOST:str
    MONGO_PORT:str
    MONGO_USER:Optional[str]
    MONGO_PASSWORD:Optional[str]

    AWS_ACCESS_KEY:str
    AWS_SECRET_ACCESS_KEY:str
    AWS_REGION_NAME:str

    BASE_PATH = Path(__file__).resolve().parent.parent

    logging.config.fileConfig(path.join(BASE_PATH, "settings", "logging.conf"), disable_existing_loggers=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

if __name__ == "__main__":
    pass
