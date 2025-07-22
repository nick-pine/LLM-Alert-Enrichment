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
logger = logging.getLogger("llm_enrichment")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not found in .env")

LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash")
HEADERS = {
    "Content-Type": "application/json",
    "x-goog-api-key": GEMINI_API_KEY
}
GEMINI_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
PROMPT_TEMPLATE_PATH = "templates/prompt_template.txt"

def clean_llm_response(text: str) -> str:
    """Cleans LLM JSON code block wrappers like ```json ...```."""
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    text = text.strip()
    if not text.startswith('{'):
        idx = text.find('{')
        if idx != -1:
            text = text[idx:]
    import re
    text = re.sub(r',([ \t\r\n]*[}\]])', r'\1', text)
    return text

def query_gemini(alert: dict, model: str = None) -> EnrichedAlertOutput:
    """
    Enriches a Wazuh alert using the Gemini API.

    Args:
        alert (dict): The alert data to enrich.
        model (str): The Gemini model to use (default: from .env).

    Returns:
        EnrichedAlertOutput: The enriched alert output schema.
    """
    if model is None:
        model = LLM_MODEL

    raw_llm_response = None
    try:
        alert_obj = WazuhAlertInput(**alert)
    except Exception as e:
        logger.error(f"Invalid alert schema: {e}")
        raise ValueError(f"Invalid input alert format: {e}")

    # Defensive YARA handling: always define yara_results
    yara_results = []
    try:
        rules = load_yara_rules()
        yara_results = scan_alert_with_yara(alert, rules)
    except Exception as e:
        logger.warning(f"YARA scan failed or no rules loaded: {e}")
        yara_results = []

    try:
        template = load_prompt_template(PROMPT_TEMPLATE_PATH)
        prompt = template.format(
            alert_json=json.dumps(alert_obj.model_dump(), indent=2),
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        start = time.time()
        response = requests.post(
            GEMINI_API_URL_TEMPLATE.format(model=model),
            headers=HEADERS,
            json=payload,
            timeout=45
        )
        response.raise_for_status()
        api_json = response.json()
        raw_llm_response = api_json["candidates"][0]["content"]["parts"][0]["text"].strip()
        enrichment_data = {}
        if raw_llm_response:
            json_text = clean_llm_response(raw_llm_response)
            try:
                enrichment_data = json.loads(json_text)
            except Exception as extract_exc:
                logger.error(f"Gemini API extraction error: {extract_exc}")
                enrichment_data = {}

        enrichment_data.update({
            "llm_model_version": model,
            "enriched_by": f"{model}@gemini-api",
            "enrichment_duration_ms": int((time.time() - start) * 1000),
            "yara_matches": yara_results,
            "raw_llm_response": raw_llm_response
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
        # Defensive: ensure yara_results is always defined
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

