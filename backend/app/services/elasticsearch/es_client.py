from elasticsearch import AsyncElasticsearch
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class ElasticsearchClient:
    """
    A singleton wrapper for the AsyncElasticsearch client.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info(f"Connecting to Elasticsearch at {settings.ELASTICSEARCH_HOST}")
            cls._instance = super().__new__(cls)
            cls._instance.client = AsyncElasticsearch(
                hosts=[settings.ELASTICSEARCH_HOST]
            )
        return cls._instance

    async def ping(self):
        """Ping Elasticsearch to check the connection."""
        try:
            await self.client.ping()
            logger.info("Successfully connected to Elasticsearch.")
            return True
        except Exception as e:
            logger.error(f"Could not connect to Elasticsearch: {e}")
            return False

    async def close(self):
        """Close the Elasticsearch connection."""
        if self._instance and hasattr(self._instance, 'client'):
            await self._instance.client.close()
            logger.info("Elasticsearch connection closed.")

es_client = ElasticsearchClient()
es = es_client.client # Expose the raw client for easy access
