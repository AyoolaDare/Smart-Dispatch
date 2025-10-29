from app.utils.logger import logger

async def create_dispatch_task(atm_id: str, engineer_id: str):
    """
    Creates a new dispatch task.
    """
    logger.info(f"Creating dispatch task for ATM {atm_id} and engineer {engineer_id}...")
    # This is a mock implementation
    return {"dispatch_id": "DISP456", "status": "created"}
