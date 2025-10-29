from app.utils.logger import logger

async def calculate_optimal_route(engineer_id: str, atm_id: str):
    """
    Calculates the optimal route for an engineer to an ATM.
    """
    logger.info(f"Calculating optimal route for engineer {engineer_id} to ATM {atm_id}...")
    # This is a mock implementation
    return {"distance": "10km", "eta": "15 minutes"}
