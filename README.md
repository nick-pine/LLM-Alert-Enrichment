# LLM-Alert-Enrichment

Enriches security alerts using multiple LLM providers (OpenAI, Gemini, Claude, Ollama) for automated context, prioritization, and actionable insights.

## Features
- Modular provider architecture
- Environment-based configuration
- Schema validation with Pydantic
- Docker-ready for production
- Sample alert and output schemas

## Setup
1. Clone the repo:
   ```sh
   git clone https://github.com/nick-pine/LLM-Alert-Enrichment.git
   cd LLM-Alert-Enrichment
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API keys.


## Testing Providers Locally
You can test enrichment output from any provider using the `test_enrichment.py` script. By default, it uses Gemini, but you can swap to OpenAI, Claude, or Ollama by changing the import at the top:

```python
from providers.gemini import query_gemini  # or query_openai, query_claude, query_ollama
```

Run the test script:
```sh
python test_enrichment.py
```

The output is formatted as a clear, report-style summary for easy review. The original alert printout is optional (commented out at the bottom of the script).

All providers must return results matching the shared output schema. If you add a new provider, ensure it follows the same pattern.

## Docker
Build and run:
```sh
docker build -t llm-enrichment .
docker run --env-file .env -v $(pwd):/app llm-enrichment
```

## Usage
Run enrichment on a sample alert:
```sh
python llm_enrichment.py --input sample_alert.json --output enriched_output.json
```

## Contributing
Pull requests welcome! Please open issues for bugs or feature requests.


