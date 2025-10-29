from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ELASTICSEARCH_HOST: Optional[str] = None
    ELASTIC_CLOUD_ID: Optional[str] = None
    ELASTIC_API_KEY: Optional[str] = None
    APP_ENV: str
    LOG_LEVEL: str

    class Config:
        env_file = ".env"

settings = Settings()
