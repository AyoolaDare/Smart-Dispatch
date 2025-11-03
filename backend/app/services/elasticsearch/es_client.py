from elasticsearch import AsyncElasticsearch
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """
    A singleton wrapper for the AsyncElasticsearch client that lazy-initializes
    the underlying AsyncElasticsearch object on first use. This avoids the
    client attempting network operations at import time.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = None
        return cls._instance

    async def _ensure_client(self):
        """Initialize the AsyncElasticsearch client if not already initialized."""
        if self._client is None:
            logger.info("Initializing AsyncElasticsearch client using Elastic Cloud configuration")
            self._client = AsyncElasticsearch(
                cloud_id=settings.ELASTIC_CLOUD_ID,
                api_key=settings.ELASTIC_API_KEY,
                request_timeout=30,  # Cloud connections might need more time
                max_retries=2,
                retry_on_timeout=True,
            )
        return self._client

    async def get_client(self):
        """Return the initialized AsyncElasticsearch client (initializes if needed)."""
        return await self._ensure_client()

    async def ping(self):
        """Ping Elasticsearch to check the connection."""
        try:
            client = await self._ensure_client()
            await client.ping()
            logger.info("Successfully connected to Elasticsearch.")
            return True
        except Exception as e:
            logger.error(f"Could not connect to Elasticsearch: {e}")
            return False

    async def close(self):
        """Close the Elasticsearch connection if it exists."""
        if self._client:
            await self._client.close()
            logger.info("Elasticsearch connection closed.")
            self._client = None


es_client = ElasticsearchClient()

