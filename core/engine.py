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
                alert_id = alert.get("id") or f"{alert.get('timestamp')}_{alert.get('rule', {}).get('id')}"
                if alert_id in seen:
                    continue
                seen.add(alert_id)

                validate_input_alert(alert)
                log(f"Enriching alert {alert_id}...", tag="+")
                enriched = query_llm(alert, model=LLM_MODEL)

                # Uncomment below to print the raw LLM provider response for debugging
                # print("[RAW LLM RESPONSE]", enriched)

                output = {
                    "alert_id": alert_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "alert": alert,
                    "enrichment": enriched.enrichment.model_dump()
                }

                validate_enriched_output(output)
                write_enriched_output(ENRICHED_OUTPUT_PATH, output)
                push_to_elasticsearch(output)
                time.sleep(1.5)

            except Exception as e:
                log(f"{e.__class__.__name__}: {e}", tag="!")
                log(f"[DEBUG] Bad line: {line[:300]}...", tag="DEBUG")
