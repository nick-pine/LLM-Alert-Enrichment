from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

class Predecoder(BaseModel):
    program_name: Optional[str]
    timestamp: Optional[str]
    hostname: Optional[str]

class Decoder(BaseModel):
    name: Optional[str]
    parent: Optional[str]
    ftscomment: Optional[str]


class Rule(BaseModel):
    id: str = Field(..., description="Rule ID")
    level: int = Field(..., description="Alert level")
    firedtimes: Optional[int]
    mail: Optional[bool]
    pci_dss: Optional[list]
    hipaa: Optional[list]
    tsc: Optional[list]
    description: Optional[str]
    groups: Optional[list]
    nist_800_53: Optional[list]
    gpg13: Optional[list]
    gdpr: Optional[list]

class WazuhAlert(BaseModel):
    id: str
    timestamp: str
    rule: Rule
    full_log: Optional[str]
    predecoder: Optional[Predecoder]
    decoder: Optional[Decoder]
    agent: Optional[Dict[str, Any]]
    manager: Optional[Dict[str, Any]]
    data: Optional[Dict[str, Any]]
    input: Optional[Dict[str, Any]]
    location: Optional[str]

    @validator('timestamp', pre=True, always=True)
    def validate_timestamp(cls, v):
        if not v or not isinstance(v, str):
            return datetime.utcnow().isoformat() + "Z"
        import re
        if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", v):
            return datetime.utcnow().isoformat() + "Z"
        return v

    @validator('id', pre=True, always=True)
    def validate_id(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("Missing or invalid alert id")
        return v
