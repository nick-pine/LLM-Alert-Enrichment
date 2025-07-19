"""
FastAPI server for the enrichment API.
Run with: uvicorn api.api_server:app --reload
"""
from fastapi import FastAPI, HTTPException, Request
from api.api_schema import EnrichRequest, EnrichResponse, ErrorResponse, Enrichment
from core.preprocessing import fill_missing_fields, normalize_alert_types
from core.io import push_to_elasticsearch
import datetime

app = FastAPI()

@app.post("/v1/enrich", response_model=EnrichResponse, responses={400: {"model": ErrorResponse}})
async def enrich_alert(request: Request):
    try:
        from providers.gemini import query_gemini
        body = await request.json()
        # Accept both wrapped and unwrapped formats
        if isinstance(body, dict) and "alert" in body and isinstance(body["alert"], dict):
            alert = body["alert"]
        else:
            alert = body
        alert = fill_missing_fields(alert)
        alert = normalize_alert_types(alert)
        enriched = query_gemini(alert)
        es_doc = {
            "alert_id": enriched.alert_id,
            "timestamp": enriched.timestamp.isoformat() if hasattr(enriched.timestamp, 'isoformat') else str(enriched.timestamp),
            "alert": enriched.alert.model_dump() if hasattr(enriched.alert, 'model_dump') else dict(enriched.alert),
            "enrichment": enriched.enrichment.model_dump() if hasattr(enriched.enrichment, 'model_dump') else dict(enriched.enrichment)
        }
        push_to_elasticsearch(es_doc)
        return EnrichResponse(
            alert_id=enriched.alert_id,
            timestamp=es_doc["timestamp"],
            alert=es_doc["alert"],
            enrichment=es_doc["enrichment"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
