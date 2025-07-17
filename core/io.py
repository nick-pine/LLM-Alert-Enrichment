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

    try:
        response = requests.post(
            f"{ELASTICSEARCH_URL}/{ENRICHED_INDEX}/_doc",
            json=doc,
            auth=(ELASTIC_USER, ELASTIC_PASS),
            verify=False
        )
        response.raise_for_status()
        log(f"Alert {doc['alert_id']} pushed to Elasticsearch", tag="\u2713")
    except Exception as e:
        log(f"Elasticsearch push failed: {e}", tag="!")