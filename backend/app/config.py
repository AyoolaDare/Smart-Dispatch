from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ELASTICSEARCH_HOST: str
    APP_ENV: str
    LOG_LEVEL: str

    class Config:
        env_file = ".env"

settings = Settings()
