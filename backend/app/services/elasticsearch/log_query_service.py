import logging
from datetime import datetime
from app.services.elasticsearch.es_client import es
from app.utils.constants import (
    TELEMETRY_INDEX_PREFIX,
    TELEMETRY_INDEX_TEMPLATE,
    TELEMETRY_INDEX_TEMPLATE_NAME,
)

logger = logging.getLogger(__name__)

async def ingest_log(log_data: dict) -> str:
    """
    Ingests a single ATM telemetry log into a daily index.

    Args:
        log_data: A dictionary containing the ATM telemetry data.

    Returns:
        The document ID of the indexed log.
    """
    try:
        # Add a timestamp and determine the daily index name
        log_data["timestamp"] = datetime.utcnow()
        index_name = f"{TELEMETRY_INDEX_PREFIX}-{datetime.utcnow().strftime('%Y.%m.%d')}"

        # Index the document
        res = await es.index(index=index_name, document=log_data)
        logger.info(f"Successfully indexed log for ATM {log_data.get('atm_id')} with doc ID {res['_id']}")
        return res["_id"]
    except Exception as e:
        logger.error(f"Error indexing log for ATM {log_data.get('atm_id')}: {e}")
        raise

async def ensure_index_template_exists():
    """
    Checks if the ATM telemetry index template exists and creates it if not.
    This ensures that new daily indices are created with the correct mapping.
    """
    try:
        template_exists = await es.indices.exists_index_template(name=TELEMETRY_INDEX_TEMPLATE_NAME)
        if not template_exists:
            logger.info(f"Index template '{TELEMETRY_INDEX_TEMPLATE_NAME}' not found. Creating it.")
            await es.indices.put_index_template(
                name=TELEMETRY_INDEX_TEMPLATE_NAME,
                body=TELEMETRY_INDEX_TEMPLATE
            )
            logger.info(f"Successfully created index template '{TELEMETRY_INDEX_TEMPLATE_NAME}'.")
        else:
            logger.info(f"Index template '{TELEMETRY_INDEX_TEMPLATE_NAME}' already exists.")
    except Exception as e:
        logger.error(f"Error ensuring index template exists: {e}")
        raise
