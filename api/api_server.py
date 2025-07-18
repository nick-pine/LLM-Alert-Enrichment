"""
FastAPI server for the enrichment API.
Run with: uvicorn api.api_server:app --reload
"""
from fastapi import FastAPI, HTTPException
from api.api_schema import EnrichRequest, EnrichResponse, ErrorResponse, Enrichment
from core.preprocessing import fill_missing_fields, normalize_alert_types
from core.io import push_to_elasticsearch
import datetime

app = FastAPI()

@app.post("/v1/enrich", response_model=EnrichResponse, responses={400: {"model": ErrorResponse}})
def enrich_alert(request: EnrichRequest):
    try:
        alert = fill_missing_fields(request.alert)
        alert = normalize_alert_types(alert)
        alert_id = alert.get("id", "unknown")
        timestamp = datetime.datetime.utcnow().isoformat()
        # Dummy enrichment for demo
        enrichment = Enrichment(
            summary_text="Enriched summary",
            tags=["test"],
            risk_score=42,
            false_positive_likelihood=0.1,
            alert_category="demo",
            remediation_steps=["step1", "step2"],
            related_cves=[],
            external_refs=[],
            llm_model_version="demo-v1",
            enriched_by="demo",
            enrichment_duration_ms=100,
            yara_matches=[],
            raw_llm_response=None,
            error=None
        )
        # Prepare document for Elasticsearch (flattened for compatibility)
        es_doc = {
            "alert_id": alert_id,
            "timestamp": timestamp,
            "alert": alert,
            "enrichment": enrichment.dict() if hasattr(enrichment, 'dict') else dict(enrichment)
        }
        push_to_elasticsearch(es_doc)
        return EnrichResponse(alert_id=alert_id, timestamp=timestamp, alert=alert, enrichment=enrichment)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
