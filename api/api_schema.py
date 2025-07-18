"""
API request/response schemas for the enrichment endpoint.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class EnrichRequest(BaseModel):
    alert: Dict[str, Any] = Field(..., description="Raw alert JSON object to enrich.")

class Enrichment(BaseModel):
    summary_text: Optional[str]
    tags: Optional[List[str]]
    risk_score: Optional[int] = Field(None, ge=0, le=100)
    false_positive_likelihood: Optional[float] = Field(None, ge=0.0, le=1.0)
    alert_category: Optional[str]
    remediation_steps: Optional[List[str]]
    related_cves: Optional[List[str]]
    external_refs: Optional[List[str]]
    llm_model_version: Optional[str]
    enriched_by: Optional[str]
    enrichment_duration_ms: Optional[int]
    yara_matches: Optional[List[Any]] = None
    raw_llm_response: Optional[str] = None
    error: Optional[str] = None

class EnrichResponse(BaseModel):
    alert_id: str
    timestamp: str
    alert: Dict[str, Any]
    enrichment: Enrichment

class ErrorResponse(BaseModel):
    error: str
    code: int
    details: Optional[str] = None
