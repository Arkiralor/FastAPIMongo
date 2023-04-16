import logging
from os import path, makedirs
from pydantic import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):

    APP_NAME: str
    APP_URI: str

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
    BASE_PATH = Path(__file__).resolve().parent.parent

    # LOG_DIR = path.join(BASE_PATH, "logs/")
    # if not path.exists(LOG_DIR):
    #     makedirs(LOG_DIR)
    # LOG_FILE = path.join(LOG_DIR, "log.log")

    logging.config.fileConfig(path.join(BASE_PATH, "settings", "logging.conf"), disable_existing_loggers=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# LOG_DIR = path.join(settings.BASE_PATH, "logs/")
# if not path.exists(LOG_DIR):
#     makedirs(LOG_DIR)
# LOG_FILE = path.join(LOG_DIR, "log.log")

if __name__ == "__main__":
    pass
