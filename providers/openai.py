"""
OpenAI provider integration for LLM enrichment.
Handles API key loading, prompt formatting, and enrichment logic.
"""
# providers/openai.py
import json
import time
import openai
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from schemas.input_schema import WazuhAlertInput
from schemas.output_schema import Enrichment, EnrichedAlertOutput
from providers.ollama import query_ollama
from core.logger import log
from core.utils import load_prompt_template
from core.yara_integration import load_yara_rules, scan_alert_with_yara
import logging

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found in .env")
openai.api_key = OPENAI_API_KEY

logger = logging.getLogger("llm_enrichment")


def query_openai(alert: dict, model: str = None) -> EnrichedAlertOutput:
    """
    Enriches a Wazuh alert using the OpenAI API.

    Args:
        alert (dict): The alert data to enrich.
        model (str): The OpenAI model to use (default: "gpt-4").

    Returns:
        EnrichedAlertOutput: The enriched alert output schema.

    Raises:
        ValueError: If the input alert format is invalid.
        RuntimeError: If the prompt template cannot be loaded.
    """

    if model is None:
        model = os.getenv("LLM_MODEL", "gpt-4")

    # Validate alert input
    try:
        alert_obj = WazuhAlertInput(**alert)
    except Exception as e:
        raise ValueError(f"Invalid input alert format: {e}")

    # YARA integration: load rules and scan alert
    yara_results = []
    try:
        rules = load_yara_rules()
        yara_results = scan_alert_with_yara(alert, rules)
    except Exception as e:
        log(f"[!] YARA scan failed or no rules loaded: {e}", tag="yara")

    # Load prompt template and include YARA results if present
    try:
        template = load_prompt_template("templates/prompt_template.txt")
    except Exception as e:
        raise RuntimeError(f"Failed to load prompt template: {e}")

    prompt = template.format(
        alert_json=json.dumps(alert_obj.model_dump(), indent=2),
        # Always keep yara_results as a list for schema consistency
    )

    try:
        start = time.time()
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        content_raw = response.choices[0].message.content
        if content_raw is None:
            raise ValueError("OpenAI response content is None")
        content = content_raw.strip()

        # Remove code block formatting if present
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        enrichment_data = json.loads(content)
        enrichment_data.update({
            "llm_model_version": model,
            "enriched_by": f"{model}@openai-api",
            "enrichment_duration_ms": int((time.time() - start) * 1000),
            "yara_matches": yara_results
        })
        enrichment = Enrichment(**enrichment_data)
        return EnrichedAlertOutput(
            alert_id=alert.get("id", "unknown-id"),
            timestamp=datetime.now(timezone.utc),
            alert=alert_obj,
            enrichment=enrichment
        )

    except Exception as e:
        logger.error(f"OpenAI error: {e}")
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
            enriched_by=f"{model}@openai-api",
            enrichment_duration_ms=0,
            yara_matches=yara_results
        )
        return EnrichedAlertOutput(
            alert_id=alert.get("id", "unknown-id"),
            timestamp=datetime.now(timezone.utc),
            alert=alert_obj,
            enrichment=fallback_enrichment
        )
