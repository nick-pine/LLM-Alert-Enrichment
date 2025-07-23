# LLM Alert Enrichment - Architecture Overview

## Directory Structure

### Current Structure (Post-Reorganization)
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
└── llm_enrichment.py      # Main entry point
```

## Component Overview

### 1. Unified Schema System (`src/schemas/`)
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

## Key Improvements Made

### 1. Debug Code Cleanup
- **Before**: Hardcoded `/tmp/debug_steps.log` files throughout codebase
- **After**: Structured logging with configurable levels and outputs
- **Benefits**: Cleaner code, configurable debugging, production-ready logging

### 2. Schema Consolidation
- **Before**: Separate files for input, output, and API schemas with duplication
- **After**: Unified schema system in `schemas/__init__.py`
- **Benefits**: Reduced duplication, easier maintenance, consistent validation

### 3. Directory Reorganization
- **Before**: Flat structure with mixed concerns
- **After**: Organized `src/` structure with clear separation of concerns
- **Benefits**: Better code organization, easier navigation, scalable structure

### 4. Configuration Unification
- **Before**: Scattered configuration across multiple files
- **After**: Centralized `config/settings.py` with Pydantic validation
- **Benefits**: Single configuration source, type safety, environment flexibility

## Development Workflow

### 1. Adding New Providers
1. Create provider class in `src/providers/`
2. Implement standardized interface
3. Add provider configuration to `config/settings.py`
4. Update factory pattern in core engine

### 2. Schema Changes
1. Update schemas in `src/schemas/__init__.py`
2. Run validation: `make validate-schemas`
3. Update affected components
4. Test with sample data

### 3. API Extensions
1. Add endpoints to `src/api/server.py`
2. Define request/response schemas in `src/api/schema.py`
3. Update OpenAPI documentation
4. Add integration tests

## Migration Notes

The migration script (`scripts/migrate_structure.py`) handles:
- Moving files to new directory structure
- Preserving file history where possible
- Creating necessary directories
- Providing migration checklist

To complete migration:
1. Run migration script
2. Update import statements in moved files
3. Test all functionality
4. Remove old empty directories
5. Update CI/CD configurations

## Best Practices

1. **Imports**: Use absolute imports from `src/` modules
2. **Configuration**: Access settings through `config.settings`
3. **Logging**: Use structured logging via `core.debug.get_debug_logger()`
4. **Schemas**: Validate all data through unified schema system
5. **Testing**: Organize tests to mirror `src/` structure
