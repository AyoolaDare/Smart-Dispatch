import logging
from app.config import settings

def setup_logger():
    """Set up the application logger."""
    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)

logger = setup_logger()
