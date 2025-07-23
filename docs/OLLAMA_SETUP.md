# Ollama Setup Instructions

This guide explains how to set up Ollama as the local LLM provider for the enrichment pipeline.

## 1. Install Ollama
Download and install Ollama from https://ollama.com/download for your platform.

**Linux/WSL:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download the installer from the official website.

## 2. Start Ollama Service
```bash
ollama serve
```
This starts the Ollama server on `http://localhost:11434`

## 3. Pull the Required Model
```bash
ollama pull llama3:8b
```
This downloads the llama3:8b model (default in our configuration).

## 4. Configure Environment
In your `.env` file:
```bash
LLM_MODEL=llama3:8b
OLLAMA_API=http://localhost:11434/api/generate
```

## 5. Test the Setup
```bash
# Test via script
python scripts/test_enrichment.py

# Test via API
curl -X POST "http://localhost:8000/v1/enrich" \
  -H "Content-Type: application/json" \
  -d '{"id": "test-123", "timestamp": "2025-07-23T12:00:00Z"}'
```

## 6. Verify in Logs
Check the application logs for successful Ollama API calls:
```
INFO: Ollama API call successful for model llama3:8b
INFO: Generated enrichment for alert test-123
```

## Available Models
Popular models you can use:
- `llama3:8b` - Default, good balance of speed and quality
- `llama3:70b` - Higher quality, requires more resources
- `mistral:7b` - Faster, smaller model
- `codellama:13b` - Specialized for code analysis

To switch models:
1. Pull the model: `ollama pull <model-name>`
2. Update `LLM_MODEL` in your `.env` file
3. Restart the application

## Troubleshooting
- **Connection refused**: Ensure `ollama serve` is running
- **Model not found**: Run `ollama pull <model-name>` first
- **Slow responses**: Consider using a smaller model like `mistral:7b`
- **Out of memory**: Use a smaller model or increase system resources
