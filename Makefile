# Makefile for LLM Alert Enrichment

.PHONY: help install test clean run-api run-enrichment docker-build docker-up docker-down lint format

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run tests
	python test_enrichment.py

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f dead_letter_queue.jsonl

run-api: ## Run the API server with new structure
	uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000

run-enrichment: ## Run the enrichment pipeline
	python llm_enrichment.py

docker-build: ## Build Docker image
	docker compose build

docker-up: ## Start Docker services
	docker compose up -d

docker-down: ## Stop Docker services
	docker compose down

lint: ## Run linting
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

format: ## Format code
	black . --line-length 100

validate-schemas: ## Validate all schema files
	python -c "from src.schemas import WazuhAlertInput, EnrichedAlertOutput; print('✅ Schemas are valid')"

check-env: ## Check environment configuration
	python -c "from config import settings; print('✅ Environment configuration loaded successfully')"
