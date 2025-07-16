
"""
Claude provider integration for LLM enrichment.
Handles API key loading, prompt formatting, and enrichment logic.
"""
# providers/claude.py
import json
import time
import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from schemas.input_schema import WazuhAlertInput
from schemas.output_schema import Enrichment, EnrichedAlertOutput
from core.yara_integration import load_yara_rules, scan_alert_with_yara
from providers.ollama import query_ollama
from core.logger import log
from core.utils import load_prompt_template

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise EnvironmentError("ANTHROPIC_API_KEY not found in .env")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

def query_claude(alert: dict, model: str = "claude-3-sonnet") -> EnrichedAlertOutput:
    """
    Enriches a Wazuh alert using the Claude API.

    Args:
        alert (dict): The alert data to enrich.
        model (str): The Claude model to use (default: "claude-3-sonnet").

    Returns:
        EnrichedAlertOutput: The enriched alert output schema.

    Raises:
        ValueError: If the input alert format is invalid.
        RuntimeError: If the prompt template cannot be loaded.
    """

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
        log(f"YARA scan failed or no rules loaded: {e}", tag="yara")

    try:
        template = load_prompt_template("templates/prompt_template.txt")
    except Exception as e:
        raise RuntimeError(f"Failed to load prompt template: {e}")

    prompt = template.format(
        alert_json=json.dumps(alert_obj.model_dump(), indent=2),
        yara_results=json.dumps(yara_results, indent=2) if yara_results else "None"
    )

    payload = {
        "model": model,
        "max_tokens": 1024,
        "temperature": 0.3,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        start = time.time()
        response = requests.post(CLAUDE_API_URL, headers=HEADERS, json=payload, timeout=45)
        response.raise_for_status()

        content = response.json()["content"][0]["text"].strip()
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        enrichment_data = json.loads(content)
        enrichment_data.update({
            "llm_model_version": model,
            "enriched_by": f"{model}@claude-api",
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
        log(f"[!] Claude error: {e}", tag="!")
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
            enriched_by=f"{model}@claude-api",
            enrichment_duration_ms=0,
            yara_matches=yara_results
        )
        return EnrichedAlertOutput(
            alert_id=alert.get("id", "unknown-id"),
            timestamp=datetime.now(timezone.utc),
            alert=alert_obj,
            enrichment=fallback_enrichment
        )
