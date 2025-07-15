
"""
Simple logger utility for the LLM enrichment project.
Prints messages with tags for easy identification.
"""
# core/logger.py

def log(message: str, tag: str = "INFO"):
    """
    Logs a message to the console with a tag.

    Args:
        message (str): The message to log.
        tag (str): A tag to identify the log type (default: "INFO").
    """
    print(f"[{tag}] {message}")