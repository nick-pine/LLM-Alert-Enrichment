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

## Usage
Run enrichment on a sample alert:
```sh
python llm_enrichment.py --input sample_alert.json --output enriched_output.json
```

## Docker
Build and run:
```sh
docker build -t llm-enrichment .
docker run --env-file .env -v $(pwd):/app llm-enrichment
```

## Contributing
Pull requests welcome! Please open issues for bugs or feature requests.

## License
See [LICENSE](LICENSE) for details.
