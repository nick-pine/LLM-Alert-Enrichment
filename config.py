# config.py
import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash")

ALERT_LOG_PATH = os.getenv("ALERT_LOG_PATH", "/var/ossec/logs/alerts/alerts.json")
ENRICHED_OUTPUT_PATH = os.getenv("ENRICHED_OUTPUT_PATH", "llm_enriched_alerts.json")

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "https://localhost:9200")
ELASTIC_USER = os.getenv("ELASTIC_USER", "admin")
ELASTIC_PASS = os.getenv("ELASTIC_PASS", "admin")
ENRICHED_INDEX = os.getenv("ENRICHED_INDEX", "wazuh-enriched-alerts")