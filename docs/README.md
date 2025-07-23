# LLM-Alert-Enrichment

Professional LLM-powered enrichment pipeline and API for Wazuh security alerts using Ollama.

## Features
- **Clean Architecture**: Organized `src/` structure with separation of concerns
- **Unified Schema System**: Centralized Pydantic validation in `src/schemas/`
- **Structured Logging**: Professional logging system replacing debug files
- **Cross-Platform**: Works seamlessly in WSL, Windows, and Linux environments
- **FastAPI Integration**: RESTful API with automatic OpenAPI documentation
- **Elasticsearch Storage**: Optional persistence and querying capabilities
- **Production Ready**: Proper configuration management and error handling

## Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env

# 3. Start API server
uvicorn src.api.server:app --reload

# 4. Test enrichment
python scripts/test_enrichment.py
```

## Documentation
Comprehensive guides available in the `docs/` folder:
- `QUICKSTART.md`: Complete setup and usage guide
- `ARCHITECTURE.md`: System architecture and design overview  
- `OLLAMA_SETUP.md`: Ollama provider configuration
- `ENVIRONMENT.md`: Environment variable configuration
- `WSL_WINDOWS_GUIDE.md`: Cross-platform development guide
- `ELASTICSEARCH_DEV_SSL.md`: SSL setup for Elasticsearch
- `DOCKER_SETUP.md`: Docker deployment guide
- `COST_MONITORING.md`: Cost monitoring recommendations
- `PERFORMANCE_TUNING.md`: Performance optimization

## Recent Updates (July 2025)
- ✅ **Major Cleanup**: Reorganized entire codebase with professional structure
- ✅ **Schema Consolidation**: Unified all schemas into `src/schemas/__init__.py`
- ✅ **Debug Cleanup**: Removed hardcoded debug files, added structured logging
- ✅ **Cross-Platform**: Full WSL and Windows compatibility
- ✅ **Import Modernization**: Clean `from src.module import` pattern throughout

See each file for details.
