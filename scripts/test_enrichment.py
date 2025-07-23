from providers.ollama import query_ollama
import json
import time
import requests
import sys
import re

USE_API = True  # Set to False for local enrichment

def fill_missing_fields(alert):
    alert.setdefault("full_log", "")
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

# Load and preprocess alert, then wrap for API compatibility
try:
    with open("sample_alert.json", "r", encoding="utf-8") as f:
        alert_json = json.load(f)
        if '_source' in alert_json:
            alert_obj = alert_json['_source']
        else:
            alert_obj = alert_json
        alert_obj = fill_missing_fields(alert_obj)
except Exception:
    alert_obj = {
        "id": "test-1",
        "timestamp": "2025-07-15T12:00:00Z",
        "rule": {
            "id": "100001",
            "description": "Test alert for malware",
            "level": 5,
            "firedtimes": 1,
            "mail": False,
            "groups": ["test"],
            "pci_dss": [],
            "gpg13": [],
            "gdpr": [],
            "hipaa": [],
            "nist_800_53": [],
            "tsc": [],
            "mitre": {
                "id": ["T1059"],
                "technique": ["Command and Scripting Interpreter"]
            },
        },
        "agent": {"id": "001", "name": "test-agent"},
        "manager": {"name": "wazuh-manager"},
        "full_log": "This is a test alert with malware present.",
        "decoder": {
            "name": "test-decoder",
            "parent": "parent-decoder",
            "ftscomment": "comment"
        },
        "predecoder": {
            "hostname": "test-host",
            "program_name": "test-program",
            "timestamp": "2025-07-15T12:00:00Z"
        },
        "location": "/var/log/test.log",
        "data": {"message": "This is a test alert with malware present."}
    }

if isinstance(alert_obj, dict) and "alert" in alert_obj and isinstance(alert_obj["alert"], dict):
    sample_alert = alert_obj
else:
    sample_alert = {"alert": alert_obj}

if USE_API:
    url = "http://localhost:8000/v1/enrich"
    response = requests.post(url, json=sample_alert)
    print(f"API Status: {response.status_code}")
    try:
        result_dict = response.json()
        enrich = result_dict.get('enrichment', {})
        # Defensive: ensure yara_matches is always a list
        if "yara_matches" not in enrich or enrich["yara_matches"] is None:
            enrich["yara_matches"] = []
    except Exception as e:
        print(f"Error parsing API response: {e}")
        sys.exit(1)
else:
    result = query_ollama(sample_alert["alert"])
    result_dict = result.model_dump()
    enrich = result_dict['enrichment']
    if "yara_matches" not in enrich or enrich["yara_matches"] is None:
        enrich["yara_matches"] = []

print("\n==============================")
print("=== Enriched Alert Summary ===")
print("==============================")
print(f"Alert ID: {result_dict.get('alert_id', 'N/A')}")
print(f"Timestamp: {result_dict.get('timestamp', 'N/A')}")
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

# Print the raw LLM response for debugging
if enrich.get("raw_llm_response"):
    print("Raw LLM Response:")
    print(enrich["raw_llm_response"])
