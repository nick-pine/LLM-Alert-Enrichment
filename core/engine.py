"""
Main enrichment engine for the LLM enrichment project.
Handles reading alerts, running enrichment, and writing output.
"""
# core/engine.py
import json
import time
from datetime import datetime, timezone
from config import (
    LLM_MODEL,
    ALERT_LOG_PATH,
    ENRICHED_OUTPUT_PATH
)
from providers.factory import get_provider
from utils.validation import validate_input_alert, validate_enriched_output
from core.io import read_alert_log, write_enriched_output, push_to_elasticsearch
from core.logger import log
from core.preprocessing import fill_missing_fields, normalize_alert_types

query_llm = get_provider()


def run_enrichment_loop():
    """
    Continuously reads alerts, enriches them using the selected LLM provider, and writes the output.

    Tracks seen alerts to avoid duplicate enrichment.
    """
    seen = set()
    log(f"Enriching with {LLM_MODEL}...", tag="*")

    with read_alert_log(ALERT_LOG_PATH) as logfile:
        while True:
            line = logfile.readline()
            if not line:
                time.sleep(1)
                continue

            line = line.strip()
            if not line or not line.startswith("{"):
                continue

            try:
                alert = json.loads(line)

                alert = fill_missing_fields(alert)
                alert = normalize_alert_types(alert)
                alert_id = alert.get("id") or f"{alert.get('timestamp')}_{alert.get('rule', {}).get('id')}"
                if alert_id in seen:
                    continue
                seen.add(alert_id)

                try:
                    validate_input_alert(alert)
                    log(f"Enriching alert {alert_id}...", tag="+")
                    enriched = query_llm(alert, model=LLM_MODEL)
                    enrichment_data = enriched.enrichment.model_dump()
                    error_note = None
                except Exception as e:
                    # Fallback: create minimal enrichment with error info
                    log(f"[FALLBACK] Creating minimal enrichment for alert {alert_id} due to validation error.", tag="!")
                    enrichment_data = {
                        "summary_text": None,
                        "tags": [],
                        "risk_score": None,
                        "false_positive_likelihood": None,
                        "alert_category": None,
                        "remediation_steps": [],
                        "related_cves": [],
                        "external_refs": [],
                        "llm_model_version": None,
                        "enriched_by": None,
                        "enrichment_duration_ms": None,
                        "yara_matches": None,
                        "raw_llm_response": None,
                        "error": f"Validation or enrichment failed: {e}"
                    }
                output = {
                    "alert_id": alert_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "alert": alert,
                    "enrichment": enrichment_data
                }

                try:
                    validate_enriched_output(output)
                except Exception as e:
                    log(f"[FALLBACK] Output schema validation failed: {e}", tag="!")
                    # Still write and push the output, even if not schema-valid
                write_enriched_output(ENRICHED_OUTPUT_PATH, output)
                push_to_elasticsearch(output)
                time.sleep(1.5)

            except Exception as e:
                log(f"{e.__class__.__name__}: {e}", tag="!")
                log(f"[DEBUG] Bad line: {line[:300]}...", tag="DEBUG")
