
"""
Pydantic schemas for enrichment API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class EnrichRequest(BaseModel):
    """Request payload for enrichment API."""
    alert: Dict[str, Any] = Field(..., description="Raw alert JSON object to enrich.")

class Enrichment(BaseModel):
    """Enrichment output schema."""
    summary_text: Optional[str] = None
    tags: Optional[List[str]] = None
    risk_score: Optional[int] = Field(None, ge=0, le=100)
    false_positive_likelihood: Optional[float] = Field(None, ge=0.0, le=1.0)
    alert_category: Optional[str] = None
    remediation_steps: Optional[List[str]] = None
    related_cves: Optional[List[str]] = None
    external_refs: Optional[List[str]] = None
    llm_model_version: Optional[str] = None
    enriched_by: Optional[str] = None
    enrichment_duration_ms: Optional[int] = None
    yara_matches: Optional[List[Any]] = None
    raw_llm_response: Optional[str] = None
    error: Optional[str] = None

class EnrichResponse(BaseModel):
    """Response payload for enrichment API."""
    alert_id: str
    timestamp: str
    alert: Dict[str, Any]
    enrichment: Enrichment

class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    code: int
    details: Optional[str] = None
