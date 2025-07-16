
"""
Output schema definitions for enriched alerts in the LLM enrichment project.
Uses Pydantic models for validation and type safety.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from schemas.input_schema import WazuhAlertInput

class Enrichment(BaseModel):
    """Schema for enrichment details returned by LLM providers."""
    summary_text: Optional[str]
    tags: Optional[List[str]]
    risk_score: Optional[int] = Field(ge=0, le=100)
    false_positive_likelihood: Optional[float] = Field(ge=0.0, le=1.0)
    alert_category: Optional[str]
    remediation_steps: Optional[List[str]]
    related_cves: Optional[List[str]]
    external_refs: Optional[List[str]]
    llm_model_version: Optional[str]
    enriched_by: Optional[str]
    enrichment_duration_ms: Optional[int]
    yara_matches: Optional[list] = None  # List of YARA match results (rule, tags, meta)
    raw_llm_response: Optional[str] = None  # For debugging: raw LLM output

class EnrichedAlertOutput(BaseModel):
    """Schema for the final enriched alert output."""
    alert_id: str
    timestamp: datetime
    alert: WazuhAlertInput
    enrichment: Enrichment
