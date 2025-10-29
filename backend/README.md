# ATM Smart Dispatch System

This is the backend for the AI-powered ATM Smart Dispatch System.

## How to Run Locally

### With a Local Elasticsearch Instance

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
    -   **macOS/Linux**: `source venv/bin/activate`
    -   **Windows**: `venv\\Scripts\\activate`
5.  **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```
6.  **Create a `.env` file** from the example:
    ```bash
    cp .env.example .env
    ```
7.  **Ensure `ELASTICSEARCH_HOST` is set** in your `.env` file.
8.  **Run the FastAPI application**:
    ```bash
    uvicorn app.main:app --reload
    ```

### With Elastic Cloud

1.  **Follow steps 2-6** from the local setup.
2.  **In your `.env` file, comment out `ELASTICSEARCH_HOST`** and set your `ELASTIC_CLOUD_ID` and `ELASTIC_API_KEY`.
3.  **Run the FastAPI application**:
    ```bash
    uvicorn app.main:app --reload
    ```

The API will be available at `http://127.0.0.1:8000`.
