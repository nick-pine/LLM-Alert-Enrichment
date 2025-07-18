# Environment Configuration

This file documents all environment variables required for the LLM enrichment pipeline and API server.

## Required Variables
- `ELASTICSEARCH_URL`: URL for Elasticsearch instance
- `ELASTIC_USER`: Elasticsearch username
- `ELASTIC_PASS`: Elasticsearch password
- `ENRICHED_INDEX`: Elasticsearch index for enriched alerts
- `ALERT_LOG_PATH`: Path to input alert log file
- `LLM_MODEL`: Provider/model to use (e.g., openai, gemini, claude, ollama)
- `ELASTIC_CA_BUNDLE`: Path to CA bundle for SSL verification

## Optional Variables
- Any provider-specific API keys or config

See `.env.example` for a template.
