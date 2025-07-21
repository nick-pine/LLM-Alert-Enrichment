# LLM-Alert-Enrichment

Provider-agnostic enrichment pipeline and API for Wazuh alerts using LLMs (OpenAI, Gemini, Claude, Ollama).

## Features
- Modular provider architecture
- Pydantic schema validation
- Docker and venv support
- Secure Elasticsearch integration
- FastAPI enrichment API
- Flexible logging utility (see `core/logger.py`)
- Cost monitoring and performance tuning guides

## Documentation
All guides and work logs are now in the `docs/` folder:
- `DOCKER_SETUP.md`: Docker setup guide
- `ELASTICSEARCH_DEV_SSL.md`: SSL setup for Elasticsearch
- `ENVIRONMENT.md`: Environment variable configuration
- `OLLAMA_SETUP.md`: Ollama provider setup
- `QUICKSTART.md`: Quickstart guide
- `COST_MONITORING.md`: Cost monitoring recommendations
- `PERFORMANCE_TUNING.md`: Performance tuning instructions

**Update (July 18, 2025):**
The enrichment API now accepts both wrapped (`{"alert": {...}}`) and unwrapped (`{...}`) alert payloads for maximum compatibility. See `QUICKSTART.md` for examples.

See each file for details.
