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
from core.factory import get_llm_query_function
from utils.validation import validate_input_alert, validate_enriched_output
from core.io import read_alert_log, write_enriched_output, push_to_elasticsearch
from core.logger import log
from core.preprocessing import fill_missing_fields, normalize_alert_types

query_llm = get_llm_query_function()


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
                    try:
                        enriched = query_llm(alert, model=LLM_MODEL)
                    except Exception as e:
                        log(f"[WARNING] LLM provider failed: {e}", tag="!")
                        enriched = None
                    enrichment_data = None
                    if enriched and hasattr(enriched, "enrichment"):
                        enrichment_data = enriched.enrichment.model_dump()
                        # Defensive: ensure yara_matches is always present
                        if "yara_matches" not in enrichment_data or enrichment_data["yara_matches"] is None:
                            enrichment_data["yara_matches"] = []
                    else:
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
                            "yara_matches": [],
                            "raw_llm_response": None,
                            "error": "Validation or enrichment failed"
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
                    import traceback
                    log(f"[FALLBACK] Output schema validation failed: {e}\nTraceback: {traceback.format_exc()}", tag="!")
                    # Still write and push the output, even if not schema-valid
                write_enriched_output(ENRICHED_OUTPUT_PATH, output)
                push_to_elasticsearch(output)
                time.sleep(1.5)

            except Exception as e:
                import traceback
                log(f"{e.__class__.__name__}: {e}\nTraceback: {traceback.format_exc()}", tag="!")
                log(f"[DEBUG] Bad line: {line[:300]}...", tag="DEBUG")
