from providers.gemini import query_gemini  # You can swap for query_openai, query_claude, or query_ollama
import json

# Example alert containing the word 'malware' to trigger the YARA rule
sample_alert = {
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


result = query_gemini(sample_alert)  # or query_ollama, query_openai, etc.


result_dict = result.model_dump()

enrich = result_dict['enrichment']

print("\n==============================")
print("=== Enriched Alert Summary ===")
print("==============================")
print(f"Alert ID: {result_dict['alert_id']}")
print(f"Timestamp: {result_dict['timestamp']}")
print("------------------------------")

enrich = result_dict['enrichment']
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

# Uncomment below to display the original alert in the output
# print("========== ORIGINAL ALERT ==========")
# print(json.dumps(result_dict['alert'], indent=2, default=str))
# print("====================================\n")
# print("========== RAW RESPONSE ==========")
# # Uncomment below to print the raw LLM provider response for debugging
# print("[RAW LLM RESPONSE]", result)
# print("====================================\n")