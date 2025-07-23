# core/utils.py

"""
Utility functions for the LLM enrichment project.
Includes decorators for safe execution and shared file loading logic.
"""

def safe_run(label="Task"):
    """
    Decorator to wrap a function with exception handling and logging.
    If the wrapped function raises an exception, it logs the error with the provided label.

    Args:
        label (str): A label to identify the task in logs.

    Returns:
        function: The decorated function with error handling.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Import logger only on error to avoid circular imports
                from src.core.logger import log
                log(f"{label} failed: {e.__class__.__name__}: {e}", tag="!")
        return wrapper
    return decorator

def load_prompt_template(path: str) -> str:
    """
    Loads and returns the prompt template from the given file path.

    Args:
        path (str): Path to the prompt template file.

    Returns:
        str: Contents of the prompt template file.

    Raises:
        RuntimeError: If the file cannot be read for any reason.
    """
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to load prompt template: {e}")