"""
Unified schema definitions for Wazuh alerts and enrichment data.
This file consolidates all Pydantic models used across the system.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# =============================================================================
# WAZUH ALERT INPUT SCHEMAS
# =============================================================================

class Rule(BaseModel):
    """Schema for Wazuh rule details."""
    level: Optional[int] = None
    description: Optional[str] = None
    id: Optional[str] = None
    firedtimes: Optional[int] = None
    mail: Optional[bool] = None
    groups: Optional[List[str]] = None
    pci_dss: Optional[List[str]] = None
    gpg13: Optional[List[str]] = None
    gdpr: Optional[List[str]] = None
    hipaa: Optional[List[str]] = None
    nist_800_53: Optional[List[str]] = None
    tsc: Optional[List[str]] = None
    mitre: Optional[Dict[str, List[str]]] = None

class Agent(BaseModel):
    """Schema for Wazuh agent details."""
    id: Optional[str] = None
    name: Optional[str] = None

class Manager(BaseModel):
    """Schema for Wazuh manager details."""
    name: Optional[str] = None

class Decoder(BaseModel):
    """Schema for Wazuh decoder details."""
    name: Optional[str] = None
    parent: Optional[str] = None
    ftscomment: Optional[str] = None

class Predecoder(BaseModel):
    """Schema for Wazuh predecoder details."""
    program_name: Optional[str] = None
    timestamp: Optional[str] = None
    hostname: Optional[str] = None

class WazuhAlertInput(BaseModel):
    """Schema for the main Wazuh alert input."""
    timestamp: str
    rule: Rule
    agent: Agent
    manager: Optional[Manager] = None
    id: str
    full_log: Optional[str] = None
    decoder: Optional[Decoder] = None
    predecoder: Optional[Predecoder] = None
    location: Optional[str] = None

    class Config:
        extra = "allow"  # Allow extra fields for future compatibility

# =============================================================================
# ENRICHMENT OUTPUT SCHEMAS
# =============================================================================

class Enrichment(BaseModel):
    """Schema for enrichment details returned by LLM providers."""
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
    yara_matches: Optional[List[Dict[str, Any]]] = None
    raw_llm_response: Optional[str] = None
    error: Optional[str] = None

class EnrichedAlertOutput(BaseModel):
    """Schema for the final enriched alert output."""
    alert_id: str
    timestamp: datetime
    alert: WazuhAlertInput
    enrichment: Enrichment

# =============================================================================
# API SCHEMAS
# =============================================================================

class EnrichRequest(BaseModel):
    """Request payload for enrichment API."""
    alert: Dict[str, Any] = Field(..., description="Raw alert JSON object to enrich.")

class EnrichResponse(BaseModel):
    """Response payload for enrichment API."""
    alert_id: str
    timestamp: str
    alert: Dict[str, Any]
    enrichment: Enrichment

class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
    timestamp: Optional[str] = None

# =============================================================================
# LEGACY COMPATIBILITY
# =============================================================================

# For backward compatibility, create aliases
WazuhAlert = WazuhAlertInput  # Legacy name used in some files

# Export all schemas
__all__ = [
    'Rule',
    'Agent', 
    'Predecoder',
    'Decoder',
    'WazuhAlertInput',
    'Enrichment',
    'EnrichedAlertOutput',
    'EnrichRequest',
    'EnrichResponse', 
    'ErrorResponse',
    'WazuhAlert'  # Legacy alias
]
