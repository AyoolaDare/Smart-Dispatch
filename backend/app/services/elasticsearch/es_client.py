from elasticsearch import AsyncElasticsearch
from app.config import settings

es = AsyncElasticsearch(hosts=[settings.ELASTICSEARCH_HOST])
