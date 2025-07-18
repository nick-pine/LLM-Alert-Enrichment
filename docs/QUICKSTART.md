# Quickstart Guide

## 1. Clone the Repository

```sh
git clone <repo-url>
cd llm_enrichment
```

## 2. Set Up Environment
- Copy `.env.example` to `.env` and fill in required values.
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

Use PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/v1/enrich" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{ "alert": { "id": "123", "timestamp": "2025-07-17T12:00:00Z" } }' | ConvertTo-Json -Depth 5
```

Or use Swagger UI at http://127.0.0.1:8000/docs
