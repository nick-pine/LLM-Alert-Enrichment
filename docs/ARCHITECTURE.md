# LLM Alert Enrichment - Architecture Overview

## Directory Structure
```
LLM-Alert-Enrichment/
├── src/                     # Source code (organized by component)
│   ├── api/                 # API server and routes
│   │   ├── server.py        # FastAPI application
│   │   └── schema.py        # API-specific schemas
│   ├── core/                # Core business logic
│   │   ├── debug.py         # Structured logging system
│   │   ├── engine.py        # Main enrichment engine
│   │   ├── io.py           # Input/output utilities
│   │   ├── logger.py       # Logging configuration
│   │   ├── preprocessing.py # Alert preprocessing
│   │   ├── utils.py        # Utility functions
│   │   ├── wazuh_alert_schema.py # Wazuh-specific schemas
│   │   └── yara_integration.py   # YARA rule integration
│   ├── providers/          # LLM provider implementations
│   │   └── ollama.py       # Ollama provider
│   └── schemas/            # Unified data schemas
│       └── __init__.py     # Consolidated schema definitions
├── config/                 # Configuration management
│   └── settings.py         # Unified settings with Pydantic
├── scripts/                # Utility scripts
│   ├── migrate_structure.py # Migration script
│   └── test_enrichment.py   # Testing utilities
├── tests/                  # Test files (organized by component)
├── templates/              # Prompt templates
│   └── prompt_template.txt
├── yara_rules/            # YARA rule definitions
│   └── example_rule.yar
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── Makefile               # Build and development commands
└── llm_enrichment.py      # Main entry point (single alert processing)

## Component Overview

### 1. Main Entry Point (`llm_enrichment.py`)
- **Purpose**: Command-line interface for processing alerts
- **Features**:
  - Single alert file processing with pretty output
  - Automatic detection of file format (single JSON vs log stream)
  - Handles Kibana export format (`_source` wrapper)
  - Uses proper preprocessing and enrichment pipeline
  - Elasticsearch storage with error handling
- **Usage**:
  ```bash
  python llm_enrichment.py  # Process ALERT_LOG_PATH file
  ```

### 2. Unified Schema System (`src/schemas/`)
- **Purpose**: Centralized data validation and type definitions
- **Key Components**:
  - `WazuhAlertInput`: Input alert validation
  - `Enrichment`: Individual enrichment data structure
  - `EnrichedAlertOutput`: Complete enriched alert output
  - `EnrichRequest/Response`: API communication schemas
- **Benefits**: 
  - Single source of truth for data structures
  - Consistent validation across components
  - Easier maintenance and updates

### 2. Provider Architecture (`src/providers/`)
- **Design**: Plugin-based LLM provider system
- **Current Providers**: Ollama (with llama3:8b model)
- **Interface**: Standardized provider interface for easy extension
- **Features**:
  - Configurable model selection
  - Error handling and retry logic
  - Response cleaning and validation

### 3. Core Engine (`src/core/`)
- **engine.py**: Main orchestration logic
- **preprocessing.py**: Alert normalization and preparation
- **logger.py**: Structured logging configuration
- **debug.py**: Development and debugging utilities
- **io.py**: File and data I/O operations
- **utils.py**: Common utility functions

### 4. API Layer (`src/api/`)
- **server.py**: FastAPI application with enrichment endpoints
- **schema.py**: API-specific request/response models
- **Features**:
  - RESTful enrichment API
  - Automatic validation
  - Error handling and status codes
  - OpenAPI documentation

### 5. Configuration Management (`config/`)
- **settings.py**: Pydantic-based configuration
- **Features**:
  - Environment variable integration
  - Type validation
  - Default value management
  - Development/production profiles

## Data Flow

1. **Input**: Wazuh alert received via API or direct processing
2. **Validation**: Alert validated against `WazuhAlertInput` schema
3. **Preprocessing**: Alert normalized and prepared for LLM
4. **Enrichment**: LLM provider generates security analysis
5. **Validation**: Output validated against `EnrichedAlertOutput` schema
6. **Storage**: Enriched alert stored in Elasticsearch
7. **Response**: API returns enriched data or status









