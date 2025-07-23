from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from datetime import datetime

class Predecoder(BaseModel):
    """Metadata extracted before decoding."""
    program_name: Optional[str]
    timestamp: Optional[str]
    hostname: Optional[str]

class Decoder(BaseModel):
    """Decoder information for the alert."""
    name: Optional[str]
    parent: Optional[str]
    ftscomment: Optional[str]

class Rule(BaseModel):
    """Wazuh rule details."""
    id: str = Field(..., description="Rule ID")
    level: int = Field(..., description="Alert level")
    firedtimes: Optional[int]
    mail: Optional[bool]
    pci_dss: Optional[List[str]]
    hipaa: Optional[List[str]]
    tsc: Optional[List[str]]
    description: Optional[str]
    groups: Optional[List[str]]
    nist_800_53: Optional[List[str]]
    gpg13: Optional[List[str]]
    gdpr: Optional[List[str]]

class WazuhAlert(BaseModel):
    """Schema for a Wazuh alert."""
    id: str
    timestamp: str
    rule: Rule
    full_log: Optional[str] = None
    predecoder: Optional[Predecoder] = None
    decoder: Optional[Decoder] = None
    agent: Optional[Dict[str, Any]] = None
    manager: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    input: Optional[Dict[str, Any]] = None
    location: Optional[str] = None

    @validator('timestamp', pre=True, always=True)
    def validate_timestamp(cls, v):
        """Ensure timestamp is ISO format, fallback to current UTC."""
        if not v or not isinstance(v, str):
            return datetime.utcnow().isoformat() + "Z"
        import re
        if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", v):
            return datetime.utcnow().isoformat() + "Z"
        return v

    @validator('id', pre=True, always=True)
    def validate_id(cls, v):
        """Ensure alert ID is present and valid."""
        if not v or not isinstance(v, str):
            raise ValueError("Missing or invalid alert id")
        return v
