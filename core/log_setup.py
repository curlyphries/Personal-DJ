import logging
import sys

def setup_logging():
    """Configures logging to output to both console and a file."""
    # Create a logger
    logger = logging.getLogger('PersonalDJ')
    logger.setLevel(logging.INFO)

    # Create a file handler
    file_handler = logging.FileHandler('personal_dj.log', mode='w')
    file_handler.setLevel(logging.INFO)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    # Avoid adding handlers if they already exist (e.g., in interactive sessions)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
