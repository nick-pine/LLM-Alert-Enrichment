
"""
Gemini provider integration for LLM enrichment.
Handles API key loading, prompt formatting, and enrichment logic.
"""
# providers/gemini.py

import os
import json
import time
import logging
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
from schemas.input_schema import WazuhAlertInput
from schemas.output_schema import Enrichment, EnrichedAlertOutput
from core.yara_integration import load_yara_rules, scan_alert_with_yara

from providers.ollama import query_ollama
from core.utils import load_prompt_template

load_dotenv()
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not found in .env")

HEADERS = {
    "Content-Type": "application/json",
    "x-goog-api-key": GEMINI_API_KEY
}

GEMINI_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
PROMPT_TEMPLATE_PATH = "templates/prompt_template.txt"




def clean_llm_response(text: str) -> str:
    """
    Cleans LLM JSON code block wrappers like ```json ...```.

    Args:
        text (str): The raw response string from the LLM.

    Returns:
        str: Cleaned string without code block formatting.
    """
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    # Remove any leading/trailing non-JSON text
    text = text.strip()
    # Try to extract JSON object if extra text is present
    if not text.startswith('{'):
        idx = text.find('{')
        if idx != -1:
            text = text[idx:]
    # Remove trailing commas before closing braces/brackets
    import re
    text = re.sub(r',([ \t\r\n]*[}\]])', r'\1', text)
    return text


def query_gemini(alert: dict, model: str = "gemini-2.0-flash") -> EnrichedAlertOutput:
    import sys
    logger.debug(f"[DEBUG] GEMINI_API_KEY: {GEMINI_API_KEY}")
    sys.stdout.flush()
    """
    Enriches a Wazuh alert using the Gemini API.

    Args:
        alert (dict): The alert data to enrich.
        model (str): The Gemini model to use (default: "gemini-2.0-flash").

    Returns:
        EnrichedAlertOutput: The enriched alert output schema.

    Raises:
        ValueError: If the input alert format is invalid.
        RuntimeError: If the prompt template cannot be loaded.
    """
    raw_llm_response = None
    try:
        alert_obj = WazuhAlertInput(**alert)
        # Alert schema validated
    except Exception as e:
        logger.error(f"[DEBUG] Alert schema validation failed: {e}")
        sys.stdout.flush()
        logger.error(f"Invalid alert schema: {e}")
        raise ValueError(f"Invalid input alert format: {e}")

    # YARA integration: load rules and scan alert
    # About to load YARA rules and scan alert
    yara_results = []
    try:
        rules = load_yara_rules()
        yara_results = scan_alert_with_yara(alert, rules)
        # YARA scan completed
    except Exception as e:
        # YARA scan failed or no rules loaded
        logger.warning(f"YARA scan failed or no rules loaded: {e}")

    # Prompt template loading and formatting debug
    # About to load prompt template
    try:
        template = load_prompt_template(PROMPT_TEMPLATE_PATH)
        # Prompt template loaded and about to format
        prompt = template.format(
            alert_json=json.dumps(alert_obj.model_dump(), indent=2),
            # Always keep yara_results as a list for schema consistency
        )
        # Prompt template formatted successfully
    except Exception as e:
        logger.error(f"[DEBUG] Prompt template loading/formatting failed: {e}")
        sys.stdout.flush()
        raise

    try:
        template = load_prompt_template(PROMPT_TEMPLATE_PATH)
        prompt = template.format(
            alert_json=json.dumps(alert_obj.model_dump(), indent=2),
            # Always keep yara_results as a list for schema consistency
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        # About to call Gemini API
        start = time.time()
        try:
            # Calling Gemini API now...
            response = requests.post(
                GEMINI_API_URL_TEMPLATE.format(model=model),
                headers=HEADERS,
                json=payload,
                timeout=45
            )
            # Gemini API call completed
        except Exception as api_exc:
            logger.error(f"[DEBUG] Gemini API call failed: {api_exc}")
            sys.stdout.flush()
            raise
        import sys
        # Gemini HTTP status and raw content (pre-raise)
        try:
            response.raise_for_status()
        except Exception as raise_exc:
            logger.error(f"[DEBUG] Gemini response.raise_for_status() exception: {raise_exc}")
            logger.error(f"[DEBUG] Gemini HTTP raw content (on exception): {response.content.decode('utf-8', errors='replace')}")
            sys.stdout.flush()
            raise

        # Print the full Gemini API response for debugging, before any extraction
        api_json = response.json()
        # Full Gemini API response (before extraction)

        # Try to extract the LLM response, but guard against missing keys
        try:
            raw_llm_response = api_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Raw Gemini LLM response
            if raw_llm_response is not None:
                json_text = clean_llm_response(raw_llm_response)
                # Cleaned Gemini LLM response (json_text)
                enrichment_data = json.loads(json_text)
            else:
                enrichment_data = {}
        except Exception as extract_exc:
            logger.error(f"[DEBUG] Gemini API extraction error: {extract_exc}")
            raw_llm_response = None
            enrichment_data = {}

        enrichment_data.update({
            "llm_model_version": model,
            "enriched_by": f"{model}@gemini-api",
            "enrichment_duration_ms": int((time.time() - start) * 1000),
            "yara_matches": yara_results,
            "raw_llm_response": raw_llm_response  # For debugging
        })

        enrichment = Enrichment(**enrichment_data)
        return EnrichedAlertOutput(
            alert_id=alert.get("id", "unknown-id"),
            timestamp=datetime.now(timezone.utc),
            alert=alert_obj,
            enrichment=enrichment
        )

    except Exception as e:
        logger.error(f"Gemini enrichment error: {e}")
        # Print the exception and, if available, the raw HTTP response content
        import sys
        logger.error(f"[DEBUG] Gemini Exception: {str(e)}")
        # Try to print the response content if it's a requests exception
        if 'response' in locals() and hasattr(response, 'content'):
            try:
                logger.error(f"[DEBUG] Gemini HTTP response content: {response.content.decode('utf-8')}")
            except Exception as decode_exc:
                logger.error(f"[DEBUG] Could not decode response content: {decode_exc}")
        sys.stdout.flush()
        fallback_enrichment = Enrichment(
            summary_text=f"Enrichment failed: {e}",
            tags=[],
            risk_score=0,
            false_positive_likelihood=1.0,
            alert_category="Unknown",
            remediation_steps=[],
            related_cves=[],
            external_refs=[],
            llm_model_version=model,
            enriched_by=f"{model}@gemini-api",
            enrichment_duration_ms=0,
            yara_matches=yara_results,
            raw_llm_response=raw_llm_response
        )
        return EnrichedAlertOutput(
            alert_id=alert.get("id", "unknown-id"),
            timestamp=datetime.now(timezone.utc),
            alert=alert_obj,
            enrichment=fallback_enrichment
        )

