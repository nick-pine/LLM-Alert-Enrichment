# Environment Configuration Guide

This guide explains how to configure the `.env` file for the LLM-Alert-Enrichment project. The `.env` file stores secrets and environment variables required for running enrichment locally or in production.

## Steps

1. **Copy the Example File**
   
   Copy `.env.example` to `.env` in the project root:
   ```sh
   cp .env.example .env
   ```

2. **Set Provider and Model**
   - `LLM_PROVIDER`: Choose which provider to use (`gemini`, `openai`, `claude`, or `ollama`).
   - `LLM_MODEL`: The model name for your chosen provider (e.g., `gemini-2.0-flash`, `gpt-4-turbo`, etc.).

3. **API Keys**
   - `GEMINI_API_KEY`: Your Gemini API key (required if using Gemini).
   - `OPENAI_API_KEY`: Your OpenAI API key (required if using OpenAI).
   - `ANTHROPIC_API_KEY`: Your Claude (Anthropic) API key (required if using Claude).

4. **Alert and Output Paths**
   - `ALERT_LOG_PATH`: Path to the input alert log file (e.g., `/var/ossec/logs/alerts/alerts.json`).
   - `ENRICHED_OUTPUT_PATH`: Path where enriched alerts will be saved (e.g., `llm_enriched_alerts.json`).

5. **Elasticsearch (Optional)**
   - `ELASTICSEARCH_URL`: URL for your Elasticsearch instance.
   - `ELASTIC_USER` / `ELASTIC_PASS`: Credentials for Elasticsearch.
   - `ENRICHED_INDEX`: Name of the Elasticsearch index for enriched alerts.

## Example

```
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-claude-api-key
ALERT_LOG_PATH=/var/ossec/logs/alerts/alerts.json
ENRICHED_OUTPUT_PATH=llm_enriched_alerts.json
ELASTICSEARCH_URL=https://localhost:9200
ELASTIC_USER=admin
ELASTIC_PASS=admin
ENRICHED_INDEX=wazuh-enriched-alerts
```

## Notes
- Only set the API key(s) for the provider(s) you plan to use.
- Never commit your real `.env` file or API keys to version control.
- For local testing, you can use the sample alert and output paths provided.

---
For more details, see the main `README.md`.
