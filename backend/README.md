# ATM Smart Dispatch System - Log Ingestion and Alert Detection

This backend service handles a critical part of the ATM Smart Dispatch System: ingesting telemetry logs from ATMs and detecting anomalies to create alerts.

## How to Run Locally

1.  **Ensure Elasticsearch is running** at `http://localhost:9200`.

2.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

3.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

4.  **Activate the virtual environment**:
    *   **macOS/Linux**: `source venv/bin/activate`
    *   **Windows**: `venv\\Scripts\\activate`

5.  **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

6.  **Create a `.env` file** from the example:
    ```bash
    cp .env.example .env
    ```

7.  **Run the FastAPI application**:
    ```bash
    uvicorn app.main:app --reload
    ```

The API will be available at `http://127.0.0.1:8000`.

## Testing the System

*   **Ingest a log (with an alert condition)**:
    ```bash
    POST http://127.0.0.1:8000/api/v1/logs/ingest
    Content-Type: application/json

    {
      "atm_id": "ATM-456",
      "status": "error",
      "uptime": 92.1,
      "cash_level": 30,
      "error_code": "PRINTER_JAM",
      "error_message": "Critical paper jam in receipt printer",
      "location": {"lat": 40.7128, "lon": -74.0060}
    }
    ```

*   **Check the alerts index in Elasticsearch**:
    You can query Elasticsearch directly to see if an alert was created:
    ```bash
    GET http://localhost:9200/alerts/_search
    ```
