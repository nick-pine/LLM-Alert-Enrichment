# LLM Alert Enrichment - Quickstart Guide

This guide will help you get up and running with the LLM Alert Enrichment pipeline on any machine or VM.

## Prerequisites
- Python 3.8 or newer
- Git
- Access to a Wazuh/Elasticsearch instance (local or remote)
- Docker (optional, for containerized setup)

## 1. Clone the Repository
```sh
git clone https://github.com/nick-pine/LLM-Alert-Enrichment.git
cd LLM-Alert-Enrichment
```

## 2. Set Up a Virtual Environment (Optional)
If you prefer to use a virtual environment instead of Docker, follow these steps:
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

## 3. Install Dependencies (Skip if using Docker)
```sh
pip install -r requirements.txt
```

## 4. Configure Environment Variables
- Copy `.env.example` to `.env` (if needed):
  ```sh
  cp .env.example .env
  ```
- Edit `.env` and set:
  - `ELASTICSEARCH_URL` to your Elasticsearch endpoint (e.g., `https://localhost:9200` or `http://<wazuh-vm-ip>:9200`)
  - `ELASTIC_USER` and `ELASTIC_PASS` to your Elasticsearch credentials
  - Any LLM API keys you want to use

## 5. Run the Enrichment Pipeline
```sh
python llm_enrichment.py
```

## Docker Usage (Alternative to venv)

You can also run the enrichment pipeline in a Docker container for maximum portability and isolation.

### 1. Build the Docker image
```sh
docker build -t llm-enrichment .
```

### 2. Configure Environment Variables
- Copy your `.env` file into the project directory (it will be copied into the container).

### 3. Run the Container
```sh
docker run --rm --env-file .env llm-enrichment
```

- You can mount volumes or override environment variables as needed.
- The container will run the enrichment pipeline just like the venv method.

## 6. Troubleshooting
- If you see SSL or authentication errors, check your `.env` settings and Elasticsearch config.
- For remote Elasticsearch, ensure network/firewall rules allow access.
- For self-signed SSL, use `verify_certs=False` in the code (already set by default).

---

**You can now enrich Wazuh alerts and send results to Elasticsearch from any machine or VM!**

For more details, see `ENVIRONMENT.md` and `README.md`.

**Choose Docker for production or sharing, and venv for local development. Both are supported!**
