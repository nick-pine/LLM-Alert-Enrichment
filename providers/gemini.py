
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
    return text


def query_gemini(alert: dict, model: str = "gemini-2.0-flash") -> EnrichedAlertOutput:
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
    try:
        alert_obj = WazuhAlertInput(**alert)
    except Exception as e:
        logger.error(f"Invalid alert schema: {e}")
        raise ValueError(f"Invalid input alert format: {e}")

    try:
        template = load_prompt_template(PROMPT_TEMPLATE_PATH)
        prompt = template.format(alert_json=json.dumps(alert_obj.model_dump(), indent=2))
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

        json_text = clean_llm_response(
            response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        )
        enrichment_data = json.loads(json_text)

        enrichment_data.update({
            "llm_model_version": model,
            "enriched_by": f"{model}@gemini-api",
            "enrichment_duration_ms": int((time.time() - start) * 1000)
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
            enrichment_duration_ms=0
        )
        return EnrichedAlertOutput(
            alert_id=alert.get("id", "unknown-id"),
            timestamp=datetime.now(timezone.utc),
            alert=alert_obj,
            enrichment=fallback_enrichment
        )

