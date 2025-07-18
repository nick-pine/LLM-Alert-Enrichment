
"""
Preprocessing utilities for the LLM enrichment project.
Handles filling missing fields and normalizing alert types.
"""

from typing import Dict, Any, Optional
import copy

# Module-level constants for defaults
PREDECODER_DEFAULTS = {
    "program_name": "",
    "timestamp": "",
    "hostname": ""
}
DECODER_DEFAULTS = {"name": "", "parent": "", "ftscomment": ""}
RULE_DEFAULTS = {
    "gpg13": [],
    "hipaa": [],
    "mitre": {"id": [], "technique": []}
}


def fill_missing_fields(
    alert: Dict[str, Any],
    predecoder_defaults: Optional[Dict[str, Any]] = None,
    decoder_defaults: Optional[Dict[str, Any]] = None,
    rule_defaults: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fill missing fields in the alert dict using provided or module-level defaults.
    Args:
        alert: The alert dictionary to process.
        predecoder_defaults: Optional custom defaults for predecoder.
        decoder_defaults: Optional custom defaults for decoder.
        rule_defaults: Optional custom defaults for rule.
    Returns:
        The alert dictionary with missing fields filled.
    """
    alert.setdefault("full_log", "")
    predecoder_defaults = predecoder_defaults or copy.deepcopy(PREDECODER_DEFAULTS)
    decoder_defaults = decoder_defaults or copy.deepcopy(DECODER_DEFAULTS)
    rule_defaults = rule_defaults or copy.deepcopy(RULE_DEFAULTS)

    # Ensure predecoder exists and has required fields
    if "predecoder" not in alert or not isinstance(alert["predecoder"], dict):
        alert["predecoder"] = copy.deepcopy(predecoder_defaults)
    else:
        for k, v in predecoder_defaults.items():
            alert["predecoder"].setdefault(k, v)

    # Ensure decoder fields
    alert.setdefault("decoder", copy.deepcopy(decoder_defaults))
    if "decoder" in alert:
        for k, v in decoder_defaults.items():
            alert["decoder"].setdefault(k, v)

    # Ensure rule fields
    if "rule" in alert:
        for k, v in rule_defaults.items():
            if isinstance(v, dict):
                alert["rule"].setdefault(k, copy.deepcopy(v))
            else:
                alert["rule"].setdefault(k, v if not isinstance(v, list) else v.copy())
    return alert



def normalize_alert_types(alert: Dict[str, Any]) -> Dict[str, Any]:
    """
    Coerce alert fields to the correct types to match the Pydantic schema and avoid mapping errors.
    Args:
        alert: The alert dictionary to process.
    Returns:
        The alert dictionary with normalized types.
    """
    # Top-level fields
    for key in ["timestamp", "id"]:
        alert[key] = str(alert.get(key, ""))
    for key in ["full_log", "location"]:
        if key in alert and alert[key] is not None:
            alert[key] = str(alert[key])

    # Rule
    rule = alert.get("rule")
    if isinstance(rule, dict):
        # Int fields
        for key in ["level", "firedtimes"]:
            if key in rule and rule[key] is not None:
                try:
                    rule[key] = int(rule[key])
                except Exception:
                    rule[key] = 0
        # String fields
        for key in ["description", "id", "mail"]:
            if key in rule and rule[key] is not None:
                rule[key] = str(rule[key])
        # List fields (optimized with comprehension)
        list_fields = ["groups", "pci_dss", "gpg13", "gdpr", "hipaa", "nist_800_53", "tsc"]
        for key in list_fields:
            if key in rule:
                if rule[key] is None:
                    rule[key] = []
                elif not isinstance(rule[key], list):
                    rule[key] = [str(rule[key])]
        # mitre
        mitre = rule.get("mitre")
        if mitre is None or not isinstance(mitre, dict):
            rule["mitre"] = {"id": [], "technique": []}
        else:
            for mkey in ["id", "technique"]:
                if mkey in mitre:
                    if mitre[mkey] is None:
                        mitre[mkey] = []
                    elif not isinstance(mitre[mkey], list):
                        mitre[mkey] = [str(mitre[mkey])]

    # Agent
    agent = alert.get("agent")
    if isinstance(agent, dict):
        for key in ["id", "name"]:
            if key in agent and agent[key] is not None:
                agent[key] = str(agent[key])

    # Manager
    manager = alert.get("manager")
    if isinstance(manager, dict) and "name" in manager and manager["name"] is not None:
        manager["name"] = str(manager["name"])

    # Decoder
    decoder = alert.get("decoder")
    if isinstance(decoder, dict):
        for key in ["name", "parent", "ftscomment"]:
            if key in decoder and decoder[key] is not None:
                decoder[key] = str(decoder[key])

    # Predecoder
    predecoder = alert.get("predecoder")
    if isinstance(predecoder, dict):
        for key in ["program_name", "timestamp", "hostname"]:
            if key in predecoder and predecoder[key] is not None:
                predecoder[key] = str(predecoder[key])

    # Data (leave as-is, can be any dict)
    return alert
