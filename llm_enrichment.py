# llm_enrichment.py

import os
import json
from core.io import get_elasticsearch_client
from config import ELASTICSEARCH_URL, ELASTIC_USER, ELASTIC_PASS, ENRICHED_INDEX
from core.engine import run_enrichment_loop
from config import ALERT_LOG_PATH
from providers.ollama import query_ollama


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

    alert.setdefault("decoder", {"name": "", "parent": "", "ftscomment": ""})
    if "decoder" in alert:
        alert["decoder"].setdefault("parent", "")
        alert["decoder"].setdefault("ftscomment", "")
    if "rule" in alert:
        alert["rule"].setdefault("gpg13", [])
        alert["rule"].setdefault("hipaa", [])
        alert["rule"].setdefault("mitre", {"id": [], "technique": []})
    return alert

def run_single_alert_file():
    # Try to load the file as a single JSON object
    with open(ALERT_LOG_PATH, 'r', encoding='utf-8') as f:
        try:
            alert = json.load(f)
            # If the alert is wrapped in _source (Kibana export), extract it
            if '_source' in alert:
                alert = alert['_source']
            alert = fill_missing_fields(alert)
            result = query_ollama(alert)  # <--- Direct call
            result_dict = result.model_dump()
            enrich = result_dict['enrichment']

            print("\n==============================")
            print("=== Enriched Alert Summary ===")
            print("==============================")
            print(f"Alert ID: {result_dict['alert_id']}")
            print(f"Timestamp: {result_dict['timestamp']}")
            print("------------------------------")

            print("\n========== ENRICHMENT ==========")
            print(f"Summary:\n  {enrich.get('summary_text','')}")
            print("------------------------------")
            print(f"Tags: {', '.join(enrich.get('tags', []))}")
            print(f"Risk Score: {enrich.get('risk_score','')}")
            print(f"False Positive Likelihood: {enrich.get('false_positive_likelihood','')}")
            print(f"Alert Category: {enrich.get('alert_category','')}")
            print("------------------------------")
            print("Remediation Steps:")
            for step in enrich.get('remediation_steps', []):
                print(f"  - {step}")
            print("------------------------------")
            print(f"Related CVEs: {', '.join(enrich.get('related_cves', []))}")
            print(f"External Refs: {', '.join(enrich.get('external_refs', []))}")
            print("------------------------------")
            print(f"LLM Model Version: {enrich.get('llm_model_version','')}")
            print(f"Enriched By: {enrich.get('enriched_by','')}")
            print(f"Enrichment Duration (ms): {enrich.get('enrichment_duration_ms','')}")
            print("------------------------------")
            print("YARA Matches:")
            for match in enrich.get('yara_matches', []):
                print(f"  - Rule: {match.get('rule','')}, Meta: {match.get('meta',{})}")
            print("==============================\n")

            # Send to Elasticsearch
            from core.io import push_to_elasticsearch
            try:
                push_to_elasticsearch(result_dict)
                print(f"[INFO] Enriched alert sent to Elasticsearch via push_to_elasticsearch (alert_id: {result_dict.get('alert_id')})")
            except Exception as e:
                print(f"[ERROR] Failed to send to Elasticsearch: {e}")
        except json.JSONDecodeError:
            print("[!] Could not parse as a single JSON object. Falling back to enrichment loop.")
            run_enrichment_loop()

if __name__ == "__main__":
    # If the alert log path is a pretty-printed single JSON, handle it; else, use the enrichment loop
    run_single_alert_file()