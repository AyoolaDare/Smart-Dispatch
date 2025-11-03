import logging
from datetime import datetime
from datetime import timedelta
from app.services.elasticsearch.es_client import es_client
from app.utils.constants import ALERTS_INDEX_NAME, TELEMETRY_INDEX_PREFIX

logger = logging.getLogger(__name__)

async def get_incident_counts(days: int = 7) -> dict:
    """
    Get counts of different types of incidents/issues over a specified time period.
    
    Args:
        days: Number of days to look back
        
    Returns:
        Dictionary containing counts of different incident types
    """
    try:
        client = await es_client.get_client()
        start_time = datetime.utcnow() - timedelta(days=days)
        
        aggs_query = {
            "query": {
                "range": {
                    "timestamp": {
                        "gte": start_time.isoformat()
                    }
                }
            },
            "aggs": {
                "total_incidents": {
                    "filter": {
                        "bool": {
                            "should": [
                                {"term": {"status": "error"}},
                                {"range": {"cash_level": {"lte": 20}}},
                                {"range": {"uptime": {"lt": 95}}}
                            ]
                        }
                    }
                },
                "error_status": {
                    "filter": {
                        "term": {"status": "error"}
                    }
                },
                "low_cash": {
                    "filter": {
                        "range": {"cash_level": {"lte": 20}}
                    }
                },
                "low_uptime": {
                    "filter": {
                        "range": {"uptime": {"lt": 95}}
                    }
                },
                "error_types": {
                    "terms": {
                        "field": "error_code.keyword",
                        "size": 10
                    }
                }
            }
        }
        
        index_pattern = f"{TELEMETRY_INDEX_PREFIX}-*"
        result = await client.search(index=index_pattern, body=aggs_query, size=0)
        
        return {
            "total_incidents": result["aggregations"]["total_incidents"]["doc_count"],
            "errors": result["aggregations"]["error_status"]["doc_count"],
            "low_cash_alerts": result["aggregations"]["low_cash"]["doc_count"],
            "low_uptime_alerts": result["aggregations"]["low_uptime"]["doc_count"],
            "error_types": {
                bucket["key"]: bucket["doc_count"]
                for bucket in result["aggregations"]["error_types"]["buckets"]
            }
        }
    except Exception as e:
        logger.error(f"Error getting incident counts: {e}")
        raise

async def create_alert(alert_data: dict) -> str:
    """
    Indexes an alert document into the alerts index.

    Args:
        alert_data: A dictionary containing the alert information.

    Returns:
        The document ID of the indexed alert.
    """
    try:
        alert_data["timestamp"] = datetime.utcnow()
        client = await es_client.get_client()
        res = await client.index(index=ALERTS_INDEX_NAME, document=alert_data)
        logger.info(f"Successfully created alert for ATM {alert_data.get('atm_id')} with doc ID {res['_id']}")
        return res["_id"]
    except Exception as e:
        logger.error(f"Error creating alert for ATM {alert_data.get('atm_id')}: {e}")
        raise

async def get_all_alerts(size: int = 100) -> list:
    """
    Retrieves all alerts from the alerts index.

    Args:
        size: The maximum number of alerts to return.

    Returns:
        A list of alert documents.
    """
    try:
        query = {"query": {"match_all": {}}}
        client = await es_client.get_client()
        res = await client.search(index=ALERTS_INDEX_NAME, body=query, size=size)
        logger.info(f"Successfully retrieved {len(res['hits']['hits'])} alerts.")
        return [hit["_source"] for hit in res["hits"]["hits"]]
    except Exception as e:
        logger.error(f"Error retrieving alerts: {e}")
        # In a real app, you might want to differentiate between "index not found" and other errors.
        # For now, we return an empty list.
        return []
