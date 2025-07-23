
"""
Validation utilities for the LLM enrichment project.
Validates input alerts and enriched output schemas using Pydantic models.
"""
# utils/validation.py
from src.schemas import WazuhAlertInput, EnrichedAlertOutput
from src.core.logger import log

def validate_input_alert(data: dict):
    """
    Validates the input alert data against the WazuhAlertInput schema.

    Args:
        data (dict): The input alert data to validate.

    Returns:
        WazuhAlertInput: The validated alert object.

    Raises:
        Exception: If validation fails.
    """
    try:
        return WazuhAlertInput(**data)
    except Exception as e:
        log(f"Invalid input schema: {e}", tag="!")
        # Log the problematic alert data (truncate if very large)
        import json
        try:
            alert_str = json.dumps(data)
        except Exception:
            alert_str = str(data)
        if len(alert_str) > 1000:
            alert_str = alert_str[:1000] + '... [truncated]'
        log(f"[DEBUG] Problematic alert: {alert_str}", tag="DEBUG")
        raise

def validate_enriched_output(data: dict):
    """
    Validates the enriched output data against the EnrichedAlertOutput schema.

    Args:
        data (dict): The enriched output data to validate.

    Returns:
        EnrichedAlertOutput: The validated enriched output object.

    Raises:
        Exception: If validation fails.
    """
    try:
        return EnrichedAlertOutput(**data)
    except Exception as e:
        log(f"Invalid enriched output schema: {e}", tag="!")
        raise