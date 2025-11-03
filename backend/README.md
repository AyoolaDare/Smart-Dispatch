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

7.  **Run the FastAPI application** (choose one):

- From inside the `backend` directory (recommended):

    ```powershell
    cd backend
    uvicorn app.main:app --reload
    ```

- From the repository root you can point to the module path:

    ```powershell
    uvicorn backend.app.main:app --reload
    ```

- Or set `PYTHONPATH` for a single command (PowerShell):

    ```powershell
    $env:PYTHONPATH = 'backend'; uvicorn app.main:app --reload
    ```

The API will be available at `http://127.0.0.1:8000`.

Note: This service requires an Elasticsearch instance reachable at `ELASTICSEARCH_HOST` (default: `http://localhost:9200`). If you don't have ES running locally you can start a single-node instance with Docker:

```powershell
docker run --name es-local -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.8.1
```

Or point `ELASTICSEARCH_HOST` in `.env` to a reachable cluster. The app will log and continue running if ES is unreachable, but features that require ES will not function until a connection is available.

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

*   **Retrieve the created alerts**:
    You can now use the new API endpoint to see if an alert was created:
    ```bash
    GET http://127.0.0.1:8000/api/v1/alerts
    ```
