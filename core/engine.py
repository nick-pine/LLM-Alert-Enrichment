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


def fill_missing_fields(alert):
    alert.setdefault("full_log", "")
    # Ensure predecoder exists and has required fields
    predecoder_defaults = {
        "program_name": "",
        "timestamp": "",
        "hostname": ""
    }
    if "predecoder" not in alert or not isinstance(alert["predecoder"], dict):
        alert["predecoder"] = predecoder_defaults.copy()
    else:
        for k, v in predecoder_defaults.items():
            alert["predecoder"].setdefault(k, v)

    # Ensure decoder fields
    alert.setdefault("decoder", {"name": "", "parent": "", "ftscomment": ""})
    if "decoder" in alert:
        alert["decoder"].setdefault("parent", "")
        alert["decoder"].setdefault("ftscomment", "")
        alert["decoder"].setdefault("name", "")
    # Ensure rule fields
    if "rule" in alert:
        alert["rule"].setdefault("gpg13", [])
        alert["rule"].setdefault("hipaa", [])
        alert["rule"].setdefault("mitre", {"id": [], "technique": []})
    return alert

# --- Type normalization helper ---
def normalize_alert_types(alert):
    """
    Coerce alert fields to the correct types to match the Pydantic schema and avoid mapping errors.
    """
    # Top-level fields
    alert['timestamp'] = str(alert.get('timestamp', ''))
    alert['id'] = str(alert.get('id', ''))
    if 'full_log' in alert and alert['full_log'] is not None:
        alert['full_log'] = str(alert['full_log'])
    if 'location' in alert and alert['location'] is not None:
        alert['location'] = str(alert['location'])

    # Rule
    if 'rule' in alert and isinstance(alert['rule'], dict):
        rule = alert['rule']
        for key in ['level', 'firedtimes']:
            if key in rule and rule[key] is not None:
                try:
                    rule[key] = int(rule[key])
                except Exception:
                    rule[key] = 0
        for key in ['description', 'id', 'mail']:
            if key in rule and rule[key] is not None:
                rule[key] = str(rule[key])
        # List fields
        for key in ['groups', 'pci_dss', 'gpg13', 'gdpr', 'hipaa', 'nist_800_53', 'tsc']:
            if key in rule:
                if rule[key] is None:
                    rule[key] = []
                elif not isinstance(rule[key], list):
                    rule[key] = [str(rule[key])]
        # mitre
        if 'mitre' in rule:
            if rule['mitre'] is None or not isinstance(rule['mitre'], dict):
                rule['mitre'] = {'id': [], 'technique': []}
            else:
                for mkey in ['id', 'technique']:
                    if mkey in rule['mitre']:
                        if rule['mitre'][mkey] is None:
                            rule['mitre'][mkey] = []
                        elif not isinstance(rule['mitre'][mkey], list):
                            rule['mitre'][mkey] = [str(rule['mitre'][mkey])]

    # Agent
    if 'agent' in alert and isinstance(alert['agent'], dict):
        agent = alert['agent']
        for key in ['id', 'name']:
            if key in agent and agent[key] is not None:
                agent[key] = str(agent[key])

    # Manager
    if 'manager' in alert and isinstance(alert['manager'], dict):
        manager = alert['manager']
        if 'name' in manager and manager['name'] is not None:
            manager['name'] = str(manager['name'])

    # Decoder
    if 'decoder' in alert and isinstance(alert['decoder'], dict):
        decoder = alert['decoder']
        for key in ['name', 'parent', 'ftscomment']:
            if key in decoder and decoder[key] is not None:
                decoder[key] = str(decoder[key])

    # Predecoder
    if 'predecoder' in alert and isinstance(alert['predecoder'], dict):
        predecoder = alert['predecoder']
        for key in ['program_name', 'timestamp', 'hostname']:
            if key in predecoder and predecoder[key] is not None:
                predecoder[key] = str(predecoder[key])

    # Data (leave as-is, can be any dict)
    return alert


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
