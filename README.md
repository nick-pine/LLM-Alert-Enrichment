<<<<<<< HEAD
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
=======

# LLM Enrichment Project

## Overview
This project enriches Wazuh alerts using various LLM providers (Gemini, OpenAI, Claude, Ollama).
It is modular, well-documented, and easy to extend for new providers or enrichment logic.

## Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure environment:**
   - Copy `.env.example` to `.env` and fill in your API keys and config values.
   - Ensure `templates/prompt_template.txt` exists and contains your prompt template.
3. **Run enrichment:**
   ```bash
   python llm_enrichment.py
   ```

## Environment Variables
See `.env.example` for all required variables and their descriptions.

## Usage
Run the main enrichment script:
```bash
python llm_enrichment.py
```

## Providers
- Gemini
- OpenAI
- Claude
- Ollama

## File Structure
- `core/` - Shared utilities and logic
- `providers/` - LLM provider integrations
- `schemas/` - Input/output schemas
- `templates/` - Prompt templates
- `utils/` - Validation utilities

## Adding a New Provider
1. Create a new file in `providers/` following the pattern of existing providers.
2. Use environment variables for API keys and configuration.
3. Add comprehensive docstrings and comments for maintainability.
4. Register the provider in the factory if needed.

## Testing
Add unit and integration tests for new logic and providers to ensure reliability.

## License
MIT
>>>>>>> e43f528 (Initial commit of LLM enrichment project)
