"""
YARA integration module for alert enrichment pipeline.
Provides functions to load YARA rules and scan alert data.
"""
# core/yara_integration.py
import yara
import os
import json
from typing import List, Dict, Any

def load_yara_rules(rules_path: str = "yara_rules/") -> yara.Rules:
    """
    Loads YARA rules from the specified directory or file.
    Args:
        rules_path (str): Path to YARA rules directory or file.
    Returns:
        yara.Rules: Compiled YARA rules object.
    Raises:
        Exception: If rules cannot be loaded or compiled.
    """
    if os.path.isdir(rules_path):
        rule_files = [os.path.join(rules_path, f) for f in os.listdir(rules_path) if f.endswith('.yar') or f.endswith('.yara')]
        rules = yara.compile(filepaths={os.path.basename(f): f for f in rule_files})
    else:
        rules = yara.compile(filepath=rules_path)
    return rules

def scan_alert_with_yara(alert: dict, rules: yara.Rules) -> List[Dict[str, Any]]:
    """
    Scans the alert JSON with YARA rules.
    Args:
        alert (dict): The alert data to scan.
        rules (yara.Rules): Compiled YARA rules.
    Returns:
        List[Dict[str, Any]]: List of YARA match results (rule name, tags, meta).
    """
    alert_json = json.dumps(alert)
    matches = rules.match(data=alert_json)
    results = []
    for match in matches:
        results.append({
            "rule": match.rule,
            "tags": match.tags,
            "meta": match.meta
        })
    return results
