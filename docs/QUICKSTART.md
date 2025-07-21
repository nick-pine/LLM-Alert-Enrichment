# Quickstart Guide

## 1. Clone the Repository

```sh
git clone <repo-url>
cd llm_enrichment
```

## 2. Set Up Environment
- Copy `.env.example` to `.env` and fill in required values.

- **Create and activate a virtual environment:**

On Linux/macOS:
```sh
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:
```sh
python -m venv .venv
.venv\Scripts\activate
```

- Install dependencies:

```sh
pip install -r requirements.txt
```

## 3. Run Enrichment Pipeline

```sh
python llm_enrichment.py
```

## 4. Run API Server

```sh
uvicorn api.api_server:app --reload
```

## 5. Test API

You can now POST either format:

**Wrapped:**
```json
{ "alert": { "id": "123", "timestamp": "2025-07-17T12:00:00Z" } }
```

**Unwrapped:**
```json
{ "id": "123", "timestamp": "2025-07-17T12:00:00Z" }
```

Use PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/enrich" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{ "alert": { "id": "123", "timestamp": "2025-07-17T12:00:00Z" } }' | ConvertTo-Json -Depth 5
```

Or:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/enrich" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{ "id": "123", "timestamp": "2025-07-17T12:00:00Z" }' | ConvertTo-Json -Depth 5
```

Or use Swagger UI at http://127.0.0.1:8000/docs
http://localhost:8000/openapi.json raw OpenAPI JSON spec
