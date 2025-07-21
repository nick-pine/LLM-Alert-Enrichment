from config import LLM_PROVIDER

try:
    from providers.gemini import query_gemini
except ImportError:
    query_gemini = None
try:
    from providers.ollama import query_ollama
except ImportError:
    query_ollama = None
try:
    from providers.claude import query_claude
except ImportError:
    query_claude = None
try:
    from providers.openai import query_openai
except ImportError:
    query_openai = None

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
