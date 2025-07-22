import os
from dotenv import load_dotenv
load_dotenv()

def get_llm_query_function():
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    print(f"[DEBUG] LLM_PROVIDER selected: {LLM_PROVIDER}")
    if LLM_PROVIDER == "gemini":
        from providers.gemini import query_gemini
        return query_gemini
    elif LLM_PROVIDER == "ollama":
        from providers.ollama import query_ollama
        return query_ollama
    elif LLM_PROVIDER == "openai":
        from providers.openai import query_openai
        return query_openai
    elif LLM_PROVIDER == "claude":
        from providers.claude import query_claude
        return query_claude
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
