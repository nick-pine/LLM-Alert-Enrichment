"""
Unified configuration management for LLM Alert Enrichment.
Centralizes all environment variables and settings.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Configuration
    llm_provider: str = Field(default="ollama", env="LLM_PROVIDER")
    llm_model: str = Field(default="llama3:8b", env="LLM_MODEL")
    ollama_api: str = Field(default="http://localhost:11434/api/generate", env="OLLAMA_API")
    
    # File Paths
    alert_log_path: str = Field(default="sample_alert.json", env="ALERT_LOG_PATH")
    enriched_output_path: str = Field(default="llm_enriched_alerts.json", env="ENRICHED_OUTPUT_PATH")
    prompt_template_path: str = Field(default="templates/prompt_template.txt", env="PROMPT_TEMPLATE_PATH")
    
    # Elasticsearch Configuration
    elasticsearch_url: str = Field(default="https://localhost:9200", env="ELASTICSEARCH_URL")
    elastic_user: str = Field(default="admin", env="ELASTIC_USER")
    elastic_pass: str = Field(default="admin", env="ELASTIC_PASS")
    enriched_index: str = Field(default="wazuh-enriched-alerts", env="ENRICHED_INDEX")
    elastic_ca_bundle: Optional[str] = Field(default=None, env="ELASTIC_CA_BUNDLE")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    debug_log_file: Optional[str] = Field(default=None, env="DEBUG_LOG_FILE")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()

# Backward compatibility - export individual variables
LLM_PROVIDER = settings.llm_provider
LLM_MODEL = settings.llm_model
OLLAMA_API = settings.ollama_api
ALERT_LOG_PATH = settings.alert_log_path
ENRICHED_OUTPUT_PATH = settings.enriched_output_path
ELASTICSEARCH_URL = settings.elasticsearch_url
ELASTIC_USER = settings.elastic_user
ELASTIC_PASS = settings.elastic_pass
ENRICHED_INDEX = settings.enriched_index
