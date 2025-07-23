# WSL/Windows Development Guide

## Overview
This codebase has been cleaned up and organized for cross-platform development. You can work from WSL, Windows, or both environments seamlessly.

## Directory Structure (Post-Cleanup)
- ✅ **All source code** is now in the `src/` directory
- ✅ **No more duplicate directories** (`core/`, `providers/`, `api/`, `schemas/` removed)
- ✅ **Clean imports** using `from src.module import ...` pattern
- ✅ **No hardcoded debug files** (no more `/tmp/debug_steps.log`)

## Running from Different Environments

### WSL (Linux Subsystem)
```bash
# Navigate to your project
cd /mnt/c/Users/nickp/api/LLM-Alert-Enrichment

# Run API server
uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000

# Run enrichment pipeline
python llm_enrichment.py

# Run tests
python scripts/test_enrichment.py

# Use make commands
make run-api
make validate-schemas
make clean
```

### Windows PowerShell/Command Prompt
```powershell
# Navigate to your project
cd "C:\Users\nickp\api\LLM-Alert-Enrichment"

# Run API server
uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000

# Run enrichment pipeline
python llm_enrichment.py

# Run tests
python scripts\test_enrichment.py

# Note: Make commands work in WSL but not Windows CMD
```

### VS Code Integration
- **Terminal**: Can use either WSL or Windows terminal
- **Python Interpreter**: Choose WSL Python or Windows Python
- **File paths**: VS Code handles path translation automatically
- **Debugging**: Works in both environments

## Path Considerations

### ✅ What We Fixed:
- **Before**: Hardcoded `/tmp/debug_steps.log` (WSL-specific)
- **After**: Configurable logging via environment variables
- **Before**: Mixed path styles throughout code
- **After**: Clean Python imports using `src.` package structure

### Environment Variables
Create a `.env` file for cross-platform configuration:
```bash
# LLM Configuration
LLM_PROVIDER=ollama
LLM_MODEL=llama3:8b
OLLAMA_BASE_URL=http://localhost:11434

# Elasticsearch Configuration  
ELASTICSEARCH_URL=https://localhost:9200
ELASTIC_USER=your-username
ELASTIC_PASS=your-password

# Logging Configuration
LOG_LEVEL=INFO
DEBUG_LOG_FILE=./debug.log  # Will work on both Windows and WSL
```

## File Structure Benefits

### Cross-Platform Compatibility
```
src/
├── api/           # API server (works same on both platforms)
├── core/          # Business logic (platform-agnostic)  
├── providers/     # LLM providers (HTTP-based, platform-agnostic)
└── schemas/       # Data validation (Pydantic, platform-agnostic)
```

### Import Pattern
All imports now use the clean pattern:
```python
# ✅ Clean, platform-agnostic imports
from src.schemas import WazuhAlertInput, EnrichedAlertOutput
from src.providers.ollama import query_ollama
from src.core.logger import log

# ❌ Old problematic imports (removed)
# from core.logger import log
# from providers.ollama import query_ollama
```

## Development Workflow

### 1. Code Editing
- Edit files in VS Code (works seamlessly with WSL)
- All paths are relative to project root
- No platform-specific hardcoded paths

### 2. Testing
```bash
# Test imports work
python -c "from src.schemas import WazuhAlertInput; print('✅ Imports work')"

# Test API
curl http://localhost:8000/docs

# Test enrichment
python scripts/test_enrichment.py
```

### 3. Deployment
- **WSL/Linux**: Use the cleaned Makefile commands
- **Windows**: Run Python commands directly
- **Docker**: Platform-agnostic containerization

## Troubleshooting

### Import Errors
If you see import errors, ensure you're running from the project root:
```bash
# Make sure you're in the right directory
pwd  # Should show .../LLM-Alert-Enrichment

# Test imports
python -c "import sys; print(sys.path[0])"  # Should show current directory
```

### Path Issues
- ✅ **Fixed**: No more hardcoded `/tmp/` paths
- ✅ **Fixed**: All logging goes through proper Python logging
- ✅ **Fixed**: Configuration via environment variables

### WSL-Specific Notes
- The old `/tmp/debug_steps.log` approach has been completely removed
- All file operations now use relative paths or environment variables
- Cross-platform logging system handles path differences automatically

## Benefits of the Cleanup

1. **Platform Independence**: Code works identically on WSL and Windows
2. **Clean Imports**: No more path confusion between environments  
3. **Professional Structure**: Organized `src/` directory
4. **Maintainable**: Single source of truth for schemas and configuration
5. **Debuggable**: Proper logging system instead of hardcoded debug files

The codebase is now truly cross-platform and production-ready! 🚀
