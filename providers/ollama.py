"""
Ollama provider integration for LLM enrichment.
Handles API endpoint, prompt formatting, and enrichment logic.
"""
# providers/ollama.py

import os
import json
import time
import logging
import requests
from datetime import datetime, timezone
from schemas.input_schema import WazuhAlertInput
from schemas.output_schema import Enrichment, EnrichedAlertOutput
from core.yara_integration import load_yara_rules, scan_alert_with_yara
from core.utils import load_prompt_template  # shared utility

logger = logging.getLogger("llm_enrichment")

OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
PROMPT_TEMPLATE_PATH = "templates/prompt_template.txt"


def clean_llm_response(raw: str) -> str:
    """
    Removes code block formatting from LLM responses.

    Args:
        raw (str): The raw response string from the LLM.

    Returns:
        str: Cleaned string without code block formatting.
    """
    if raw.startswith("```"):
        raw = raw.replace("```json", "").replace("```", "").strip()
    return raw


def query_ollama(alert: dict, model: str = None) -> EnrichedAlertOutput:
    """
    Enriches a Wazuh alert using the Ollama API.

    Args:
        alert (dict): The alert data to enrich.
        model (str, optional): The Ollama model to use. If not provided, uses OLLAMA_MODEL from env.

    Returns:
        EnrichedAlertOutput: The enriched alert output schema.

    Raises:
        ValueError: If the input alert format is invalid.
        RuntimeError: If the prompt template cannot be loaded.
    """
    if model is None:
        model = os.getenv("OLLAMA_MODEL", "phi3:mini")

    try:
        alert_obj = WazuhAlertInput(**alert)
    except Exception as e:
        logger.error(f"Invalid input alert format: {e}")
        raise ValueError(f"Invalid input alert format: {e}")

    # YARA integration: load rules and scan alert
    yara_results = []
    try:
        rules = load_yara_rules()
        yara_results = scan_alert_with_yara(alert, rules)
    except Exception as e:
        logger.warning(f"YARA scan failed or no rules loaded: {e}")

    try:
        template = load_prompt_template(PROMPT_TEMPLATE_PATH)
        prompt = template.format(
            alert_json=json.dumps(alert_obj.model_dump(), indent=2),
            yara_results=json.dumps(yara_results, indent=2) if yara_results else "None"
        )

        start = time.time()
        response = requests.post(
            OLLAMA_API,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=45
        )
        response.raise_for_status()

        raw = response.json().get("response", "").strip()
        parsed_json = json.loads(clean_llm_response(raw))

        parsed_json.update({
            "llm_model_version": model,
            "enriched_by": f"{model}@ollama-api",
            "enrichment_duration_ms": int((time.time() - start) * 1000),
            "yara_matches": yara_results
        })
        enrichment = Enrichment(**parsed_json)
        return EnrichedAlertOutput(
            alert_id=alert.get("id", "unknown-id"),
            timestamp=datetime.now(timezone.utc),
            alert=alert_obj,
            enrichment=enrichment
        )

    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Ollama returned invalid JSON: {e}")
    except requests.RequestException as e:
        logger.error(f"Ollama API request failed: {e}")
    except Exception as e:
        logger.error(f"Ollama enrichment error: {e}")
        fallback = Enrichment(
            summary_text=f"Ollama enrichment failed.",
            tags=[],
            risk_score=0,
            false_positive_likelihood=1.0,
            alert_category="Unknown",
            remediation_steps=[],
            related_cves=[],
            external_refs=[],
            llm_model_version=model,
            enriched_by=f"{model}@ollama-api",
            enrichment_duration_ms=0,
            yara_matches=yara_results
        )

        return EnrichedAlertOutput(
            alert_id=alert.get("id", "unknown-id"),
            timestamp=datetime.now(timezone.utc),
            alert=alert_obj,
            enrichment=fallback
        )

