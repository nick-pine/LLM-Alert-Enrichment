from elasticsearch import Elasticsearch
import os

def get_elasticsearch_client():
    """
    Returns an Elasticsearch client.
    Uses a CA bundle for SSL verification if ELASTIC_CA_BUNDLE is set.
    Falls back to verify_certs=False with a warning if not set (not recommended for production).
    """
    from config import ELASTICSEARCH_URL, ELASTIC_USER, ELASTIC_PASS
    ca_bundle = os.getenv("ELASTIC_CA_BUNDLE")
    if ca_bundle:
        log(f"Using CA bundle for Elasticsearch SSL: {ca_bundle}", tag="i")
        return Elasticsearch(
            ELASTICSEARCH_URL,
            basic_auth=(ELASTIC_USER, ELASTIC_PASS),
            ca_certs=ca_bundle,
            headers={"Content-Type": "application/json"}
        )
    else:
        log("No CA bundle set. SSL verification is disabled (not recommended for production).", tag="!")
        return Elasticsearch(
            ELASTICSEARCH_URL,
            basic_auth=(ELASTIC_USER, ELASTIC_PASS),
            verify_certs=False,
            headers={"Content-Type": "application/json"}
        )

# core/io.py
"""
I/O utilities for the LLM enrichment project.
Handles reading alert logs, writing enriched output, and pushing to Elasticsearch.
"""
import json
import requests
from core.logger import log

def read_alert_log(path):
    """
    Opens the alert log file for reading.

    Args:
        path (str): Path to the alert log file.

    Returns:
        file object: Opened file object for reading.
    """
    return open(path, mode="r", encoding="utf-8", errors="ignore")

def write_enriched_output(path, data):
    """
    Appends enriched alert data to the output file as a JSON line.

    Args:
        path (str): Path to the output file.
        data (dict): Enriched alert data to write.
    """
    try:
        with open(path, "a") as f:
            f.write(json.dumps(data) + "\n")
        log(f"Wrote enriched alert {data['alert_id']} to file", tag="\u2192")
    except Exception as e:
        log(f"Failed to write to {path}: {e}", tag="!")

def push_to_elasticsearch(doc):
    """
    Pushes an enriched alert document to Elasticsearch.

    Args:
        doc (dict): The enriched alert document to push.
    """
    from config import ELASTICSEARCH_URL, ELASTIC_USER, ELASTIC_PASS, ENRICHED_INDEX

    import datetime
    def json_serial(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    import time
    start_time = time.time()
    try:
        # Ensure document is wrapped in "alert" field
        if "alert" not in doc:
            doc = {"alert": doc}
        # Remove reserved OpenSearch fields from alert
        reserved = ["_index", "_id", "_version", "_score", "_source", "fields", "sort", "highlight"]
        for field in reserved:
            if field in doc["alert"]:
                del doc["alert"][field]
        doc_json = json.loads(json.dumps(doc, default=json_serial))
        log(f"[DEBUG] Elasticsearch payload: {json.dumps(doc_json)[:1000]}", tag="i")
        response = requests.post(
            f"{ELASTICSEARCH_URL}/{ENRICHED_INDEX}/_doc",
            json=doc_json,
            auth=(ELASTIC_USER, ELASTIC_PASS),
            verify=False
        )
        log(f"[DEBUG] Elasticsearch response status: {response.status_code}", tag="i")
        log(f"[DEBUG] Elasticsearch response body: {response.text[:1000]}", tag="i")
        response.raise_for_status()
        elapsed = int((time.time() - start_time) * 1000)
        log(f"Alert {doc.get('alert_id', doc.get('alert', {}).get('alert_id', 'unknown'))} pushed to Elasticsearch in {elapsed}ms", tag="\u2713")
    except Exception as e:
        import traceback
        log(f"Elasticsearch push failed: {e}", tag="!")
        log(f"[DEBUG] Elasticsearch exception traceback: {traceback.format_exc()}", tag="!")