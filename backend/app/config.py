from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    Uses Elastic Cloud for Elasticsearch connection.
    """
    # Elastic Cloud configuration (required)
    ELASTIC_CLOUD_ID: str
    ELASTIC_API_KEY: str
    
    # App settings
    APP_ENV: str = "development"
    LOG_LEVEL: str = "info"

    # Use pydantic v2 style `model_config` so extra environment variables
    # present in a local `.env` file don't cause validation errors.
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }
    
    @property
    def use_elastic_cloud(self) -> bool:
        """Return True if Elastic Cloud configuration is provided."""
        return bool(self.ELASTIC_CLOUD_ID and self.ELASTIC_API_KEY)

settings = Settings()
