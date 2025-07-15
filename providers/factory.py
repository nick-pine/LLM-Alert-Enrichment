from config import LLM_PROVIDER

from providers.gemini import query_gemini
from providers.ollama import query_ollama
from providers.claude import query_claude
from providers.openai import query_openai

def get_provider():
    if LLM_PROVIDER == "gemini":
        return query_gemini
    elif LLM_PROVIDER == "ollama":
        return query_ollama
    elif LLM_PROVIDER == "claude":
        return query_claude
    elif LLM_PROVIDER == "openai":
        return query_openai
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")
