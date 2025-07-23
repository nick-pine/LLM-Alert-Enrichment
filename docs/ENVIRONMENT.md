# Environment Configuration

This file documents all environment variables required for the LLM enrichment pipeline and API server.

## Core LLM Configuration
- `LLM_MODEL`: Model to use (default: `llama3:8b`)
- `OLLAMA_API`: Ollama API endpoint (default: `http://localhost:11434/api/generate`)

## File Paths
- `ALERT_LOG_PATH`: Path to input alert log file (default: `sample_alert.json`)
- `ENRICHED_OUTPUT_PATH`: Path for enriched output (default: `llm_enriched_alerts.json`)

## Elasticsearch Configuration (Optional)
- `ELASTICSEARCH_URL`: URL for Elasticsearch instance (default: `https://localhost:9200`)
- `ELASTIC_USER`: Elasticsearch username (default: `admin`)
- `ELASTIC_PASS`: Elasticsearch password (default: `admin`)
- `ENRICHED_INDEX`: Elasticsearch index for enriched alerts (default: `wazuh-enriched-alerts`)
- `ELASTIC_CA_BUNDLE`: Path to CA bundle for SSL verification (optional)

## Development Configuration
- `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) (default: `INFO`)
- `DEBUG_LOG_FILE`: Optional debug log file path

## Setup Instructions
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` with your specific values
3. The application will automatically load these variables

## Notes
- All variables have sensible defaults for local development
- Only Ollama configuration is required for basic functionality
- Elasticsearch variables are optional (used for storage/persistence)
- The unified configuration system in `config/settings.py` handles all environment variables
