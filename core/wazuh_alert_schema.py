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

class WazuhAlert(BaseModel):
    id: str
    timestamp: str
    rule_id: Optional[int]
    level: Optional[int]
    full_log: Optional[str]
    predecoder: Optional[Predecoder]
    decoder: Optional[Decoder]
    # Add other fields as needed

    @validator('timestamp', pre=True, always=True)
    def validate_timestamp(cls, v):
        if not v or not isinstance(v, str):
            return datetime.utcnow().isoformat() + "Z"
        # Accept ISO format only
        import re
        if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", v):
            return datetime.utcnow().isoformat() + "Z"
        return v

    @validator('id', pre=True, always=True)
    def validate_id(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("Missing or invalid alert id")
        return v

    @validator('level')
    def validate_level(cls, v):
        if v is not None and (v < 1 or v > 16):
            raise ValueError("Alert level must be between 1 and 16")
        return v

    @validator('rule_id')
    def validate_rule_id(cls, v):
        if v is not None and v < 0:
            raise ValueError("Rule ID must be positive")
        return v
