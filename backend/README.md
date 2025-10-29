# ATM Smart Dispatch System

This is the backend for the AI-powered ATM Smart Dispatch System.

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
7.  **Run the FastAPI application**:
    ```bash
    uvicorn app.main:app --reload
    ```

The API will be available at `http://127.0.0.1:8000`.
