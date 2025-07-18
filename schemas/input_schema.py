
"""
Input schema definitions for Wazuh alerts in the LLM enrichment project.
Uses Pydantic models for validation and type safety.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Rule(BaseModel):
    """Schema for Wazuh rule details."""
    level: Optional[int]
    description: Optional[str]
    id: Optional[str]
    firedtimes: Optional[int]
    mail: Optional[bool]
    groups: Optional[List[str]]
    pci_dss: Optional[List[str]]
    gpg13: Optional[List[str]]
    gdpr: Optional[List[str]]
    hipaa: Optional[List[str]]
    nist_800_53: Optional[List[str]]
    tsc: Optional[List[str]]
    mitre: Optional[Dict[str, List[str]]]

class Agent(BaseModel):
    """Schema for Wazuh agent details."""
    id: Optional[str]
    name: Optional[str]

class Manager(BaseModel):
    """Schema for Wazuh manager details."""
    name: Optional[str]

class Decoder(BaseModel):
    """Schema for Wazuh decoder details."""
    name: Optional[str]
    parent: Optional[str]
    ftscomment: Optional[str]

class Predecoder(BaseModel):
    """Schema for Wazuh predecoder details."""
    program_name: Optional[str]
    timestamp: Optional[str]
    hostname: Optional[str]

class WazuhAlertInput(BaseModel):
    """Schema for the main Wazuh alert input."""
    timestamp: str
    rule: Rule
    agent: Agent
    manager: Optional[Manager]
    id: str
    full_log: Optional[str]
    decoder: Optional[Decoder]
    predecoder: Optional[Predecoder]
    location: Optional[str]

    class Config:
        extra = "allow"  # Allow extra fields for future compatibility
