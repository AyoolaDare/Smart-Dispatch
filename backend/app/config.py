from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from the environment.
    """
    ELASTICSEARCH_HOST: str = "http://localhost:9200"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
