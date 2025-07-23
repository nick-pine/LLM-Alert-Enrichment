
"""
Simple logger utility for the LLM enrichment project.
Prints messages with tags for easy identification.
"""

import logging
import sys

# Configure root logger once (console + optional file)
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        # Uncomment below to enable file logging
        # logging.FileHandler("llm_enrichment.log")
    ]
)

def log(message: str, tag: str = "INFO"):
    """
    Logs a message with a tag, using Python's logging module.

    Args:
        message (str): The message to log.
        tag (str): A tag to identify the log type (default: "INFO").
    """
    level_map = {
        "INFO": logging.INFO,
        "i": logging.INFO,
        "DEBUG": logging.DEBUG,
        "d": logging.DEBUG,
        "WARNING": logging.WARNING,
        "!": logging.WARNING,
        "ERROR": logging.ERROR,
        "e": logging.ERROR,
        "SUCCESS": logging.INFO,
        "\u2713": logging.INFO,
        "\u2192": logging.INFO,
    }
    log_level = level_map.get(tag, logging.INFO)
    logging.log(log_level, f"[{tag}] {message}")