import logging
from datetime import datetime, timedelta
from app.services.elasticsearch.es_client import es_client
from app.services.elasticsearch.alert_service import create_alert
from app.utils.constants import ALERT_RULES, TELEMETRY_INDEX_PREFIX

logger = logging.getLogger(__name__)

async def check_single_log(log_data: dict):
    """
    Checks a single telemetry log in real-time to see if it triggers any alert rules.

    Args:
        log_data: The dictionary containing the log data.
    """
    error_code = log_data.get("error_code")
    if error_code in ALERT_RULES:
        rule_details = ALERT_RULES[error_code]
        alert = {
            "atm_id": log_data.get("atm_id"),
            "rule": rule_details["rule"],
            "severity": rule_details["severity"],
            "telemetry": log_data,
        }
        await create_alert(alert)

async def run_rule_checks(window_minutes: int = 5):
    """
    Queries the last few minutes of telemetry data to find logs that match
    alert rules. This is used by the scheduler to catch any missed alerts.

    Args:
        window_minutes: The time window in minutes to check for rule violations.
    """
    logger.info(f"Running scheduled alert check for the last {window_minutes} minutes...")

    start_time = datetime.utcnow() - timedelta(minutes=window_minutes)

    # Query for documents with a matching error code within the time window
    query = {
        "query": {
            "bool": {
                "must": [
                    {"range": {"timestamp": {"gte": start_time.isoformat()}}},
                    {"terms": {"error_code.keyword": list(ALERT_RULES.keys())}}
                ]
            }
        }
    }

    try:
        index_pattern = f"{TELEMETRY_INDEX_PREFIX}-*"
        client = await es_client.get_client()
        res = await client.search(index=index_pattern, body=query, size=100) # Capping at 100 for safety

        for hit in res["hits"]["hits"]:
            log_data = hit["_source"]
            # To avoid creating duplicate alerts, we could add a check here.
            # For this implementation, we will assume a simple re-alert is acceptable.
            await check_single_log(log_data)

        logger.info(f"Scheduled alert check completed. Found {len(res['hits']['hits'])} matching logs.")

    except Exception as e:
        logger.error(f"Error during scheduled alert check: {e}")
