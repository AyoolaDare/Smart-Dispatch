from elasticsearch import AsyncElasticsearch
from app.config import settings
from app.utils.logger import logger

if settings.ELASTIC_CLOUD_ID and settings.ELASTIC_API_KEY:
    logger.info("Connecting to Elasticsearch using Cloud ID")
    es = AsyncElasticsearch(
        cloud_id=settings.ELASTIC_CLOUD_ID,
        api_key=settings.ELASTIC_API_KEY,
    )
elif settings.ELASTICSEARCH_HOST:
    logger.info(f"Connecting to Elasticsearch at {settings.ELASTICSEARCH_HOST}")
    es = AsyncElasticsearch(hosts=[settings.ELASTICSEARCH_HOST])
else:
    raise ValueError("Elasticsearch connection not configured. Please set either ELASTICSEARCH_HOST or ELASTIC_CLOUD_ID and ELASTIC_API_KEY.")
