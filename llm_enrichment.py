#!/usr/bin/env python3
"""
Main entry point for LLM Alert Enrichment.
Processes Wazuh alerts using the core enrichment engine.
"""

import os
import json
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.engine import run_enrichment_loop
from src.core.preprocessing import fill_missing_fields, normalize_alert_types
from src.providers.ollama import query_ollama
from src.core.io import push_to_elasticsearch
from config import ALERT_LOG_PATH

def process_single_alert():
    """
    Process a single alert file using the proper enrichment pipeline.
    Uses the same logic as the engine but for single-file processing.
    """
    try:
        # Read the alert file
        with open(ALERT_LOG_PATH, 'r', encoding='utf-8') as f:
            alert_data = json.load(f)
        
        # Handle Kibana export format (wrapped in _source)
        if '_source' in alert_data:
            alert_data = alert_data['_source']
        
        print(f"📋 Processing alert from: {ALERT_LOG_PATH}")
        
        # Use proper preprocessing pipeline
        alert_data = fill_missing_fields(alert_data)
        alert_data = normalize_alert_types(alert_data)
        
        print("🤖 Calling LLM for enrichment...")
        
        # Use the provider through proper interface
        enriched_result = query_ollama(alert_data)
        result_dict = enriched_result.model_dump()
        
        # Display results
        display_enrichment_results(result_dict)
        
        # Store results
        try:
            push_to_elasticsearch(result_dict)
            print(f"✅ Enriched alert sent to Elasticsearch (ID: {result_dict.get('alert_id')})")
        except Exception as e:
            print(f"⚠️  Elasticsearch storage failed: {e}")
            print("💾 Results displayed above but not stored")
        
        return result_dict
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse {ALERT_LOG_PATH} as JSON: {e}")
        print("🔄 Falling back to continuous enrichment loop...")
        run_enrichment_loop()
    except FileNotFoundError:
        print(f"❌ Alert file not found: {ALERT_LOG_PATH}")
        print("💡 Make sure the file exists or update ALERT_LOG_PATH in your .env")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise

def display_enrichment_results(result_dict):
    """Display enrichment results in a formatted way."""
    enrichment = result_dict.get('enrichment', {})
    
    print("\n" + "="*60)
    print("🔍 ENRICHMENT RESULTS")
    print("="*60)
    
    print(f"📊 Alert ID: {result_dict.get('alert_id', 'N/A')}")
    print(f"⏰ Timestamp: {result_dict.get('timestamp', 'N/A')}")
    print("-" * 60)
    
    print(f"\n📝 Summary:")
    print(f"   {enrichment.get('summary_text', 'No summary available')}")
    
    print(f"\n🏷️  Tags: {', '.join(enrichment.get('tags', []))}")
    print(f"⚠️  Risk Score: {enrichment.get('risk_score', 'N/A')}")
    print(f"🎯 False Positive Likelihood: {enrichment.get('false_positive_likelihood', 'N/A')}")
    print(f"📂 Alert Category: {enrichment.get('alert_category', 'N/A')}")
    
    print(f"\n🛠️  Remediation Steps:")
    for i, step in enumerate(enrichment.get('remediation_steps', []), 1):
        print(f"   {i}. {step}")
    
    cves = enrichment.get('related_cves', [])
    if cves:
        print(f"\n🔓 Related CVEs: {', '.join(cves)}")
    
    refs = enrichment.get('external_refs', [])
    if refs:
        print(f"🔗 External References: {', '.join(refs)}")
    
    yara_matches = enrichment.get('yara_matches', [])
    if yara_matches:
        print(f"\n🎯 YARA Matches:")
        for match in yara_matches:
            print(f"   - Rule: {match.get('rule', 'Unknown')}")
            print(f"     Meta: {match.get('meta', {})}")
    
    print(f"\n🤖 Model: {enrichment.get('llm_model_version', 'N/A')}")
    print(f"⚡ Duration: {enrichment.get('enrichment_duration_ms', 'N/A')} ms")
    print(f"🔧 Enriched by: {enrichment.get('enriched_by', 'N/A')}")
    print("="*60)

def main():
    """Main entry point."""
    print("🚀 LLM Alert Enrichment System")
    print("-" * 40)
    
    if not os.path.exists(ALERT_LOG_PATH):
        print(f"⚠️  Alert file not found: {ALERT_LOG_PATH}")
        print("💡 Create a sample alert or update ALERT_LOG_PATH in your .env")
        return
    
    # Check if it's a single alert file or log stream
    try:
        with open(ALERT_LOG_PATH, 'r') as f:
            content = f.read().strip()
            if content.startswith('{') and content.endswith('}'):
                # Single JSON object
                print("📄 Processing single alert file...")
                process_single_alert()
            else:
                # Multi-line log file
                print("📜 Processing alert log stream...")
                run_enrichment_loop()
    except Exception as e:
        print(f"❌ Error reading alert file: {e}")

if __name__ == "__main__":
    main()