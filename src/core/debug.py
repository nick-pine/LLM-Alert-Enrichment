"""
Debug utilities for the LLM enrichment system.
Provides structured logging instead of hardcoded debug files.
"""
import logging
import os
from typing import Optional

def get_debug_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a configured debug logger.
    
    Args:
        name: Logger name (usually __name__)
        level: Log level override (defaults to environment or INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Only configure if not already configured
        # Get log level from environment or use INFO as default
        log_level = level or os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # Create console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Optionally add file handler if DEBUG_LOG_FILE is set
        debug_file = os.getenv("DEBUG_LOG_FILE")
        if debug_file:
            file_handler = logging.FileHandler(debug_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    return logger

def log_step(logger: logging.Logger, step: str, data: Optional[dict] = None):
    """
    Log a processing step with optional data.
    
    Args:
        logger: Logger instance
        step: Step description
        data: Optional data to include
    """
    if data:
        logger.debug(f"STEP: {step} - Data: {data}")
    else:
        logger.debug(f"STEP: {step}")
