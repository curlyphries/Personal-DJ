from loguru import logger
from core import error_handler  # Ensure logger sinks configured once

def setup_logging():
    """Returns the shared Loguru logger configured in `core.error_handler`."""
    return logger
